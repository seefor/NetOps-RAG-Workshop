from __future__ import annotations

import argparse
import importlib.util
from importlib.metadata import PackageNotFoundError, version
import os
from pathlib import Path
import shutil
import subprocess
import sys

import yaml


BONUS = Path(__file__).resolve().parents[1]
ROOT = BONUS.parents[1]
DEFAULT_PROFILE = "netops-workshop"
DEFAULT_PROJECT = "NetOps RAG Workshop"


def hermes_base_home() -> Path:
    override = os.getenv("HERMES_HOME")
    if override:
        return Path(override).expanduser().absolute()
    return (Path.home() / ".hermes").absolute()


def profile_home(profile: str) -> Path:
    base = hermes_base_home()
    return base if profile == "default" else base / "profiles" / profile


def check(label: str, ok: bool, detail: str) -> bool:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: {detail}")
    return ok


def run(cmd: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)


def load_register_module():
    script = BONUS / "scripts" / "register_global_mcp.py"
    spec = importlib.util.spec_from_file_location("register_global_mcp", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description="Preflight Hermes Desktop NetOps bonus")
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--skip-hermes-mcp-test", action="store_true")
    args = parser.parse_args()

    results: list[bool] = []
    print(f"Platform: {sys.platform}")
    print(f"Workshop: {ROOT}")
    print(f"Profile: {args.profile}")
    print(f"Project: {args.project}\n")

    results.append(check("Python", sys.version_info >= (3, 10), sys.version.split()[0]))
    results.append(check("Workshop .env", (ROOT / ".env").exists(), str(ROOT / ".env")))
    results.append(check("Workshop package", (ROOT / "src" / "netops_rag").exists(), str(ROOT / "src" / "netops_rag")))

    hermes = shutil.which("hermes")
    results.append(check("Hermes executable", hermes is not None, hermes or "not on PATH"))
    if hermes:
        ver = run([hermes, "--version"], timeout=30)
        detail = (ver.stdout or ver.stderr).strip().splitlines()[-1] if (ver.stdout or ver.stderr).strip() else f"exit={ver.returncode}"
        results.append(check("Hermes version", ver.returncode == 0, detail))

    home = profile_home(args.profile)
    config_path = home / "config.yaml"
    results.append(check("Desktop profile", home.exists(), str(home)))
    results.append(check("Profile config", config_path.exists(), str(config_path)))

    config = {}
    if config_path.exists():
        try:
            config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            results.append(check("Profile YAML", isinstance(config, dict), "parsed"))
        except Exception as exc:
            results.append(check("Profile YAML", False, str(exc)))

    terminal = config.get("terminal", {}) if isinstance(config, dict) else {}
    results.append(check("Profile working directory", terminal.get("cwd") == str(ROOT.resolve()), str(terminal.get("cwd"))))

    profile_servers = config.get("mcp_servers", {}) if isinstance(config, dict) else {}
    stale_profile_mcp = any(name in profile_servers for name in ("netops_rag", "network_state")) if isinstance(profile_servers, dict) else False
    results.append(check("No stale profile-scoped workshop MCP", not stale_profile_mcp, "clean" if not stale_profile_mcp else "re-run desktop_profile_setup.py"))

    skills = config.get("skills", {}) if isinstance(config, dict) else {}
    external_dirs = skills.get("external_dirs", []) if isinstance(skills, dict) else []
    expected_skill_dir = str((BONUS / "hermes" / "skills").resolve())
    results.append(check("External skill directory", expected_skill_dir in external_dirs, expected_skill_dir))
    results.append(check("Skill write approval", skills.get("write_approval") is True if isinstance(skills, dict) else False, str(skills.get("write_approval") if isinstance(skills, dict) else None)))

    if hermes:
        project = run([hermes, "-p", args.profile, "project", "list"], timeout=30)
        project_output = (project.stdout + project.stderr).strip()
        project_ok = project.returncode == 0 and args.project.lower() in project_output.lower()
        results.append(check("Hermes project", project_ok, args.project if project_ok else project_output[-500:] or "missing"))

        listing = run([hermes, "mcp", "list"], timeout=30)
        list_output = listing.stdout + listing.stderr
        for name in ("netops_rag", "network_state"):
            results.append(check(f"Global MCP {name}", name in list_output, "visible to hermes mcp list" if name in list_output else "missing"))

    try:
        register = load_register_module()
        global_path = register.find_actual_global_config()
        global_config = register.load_yaml(global_path)
        servers = global_config.get("mcp_servers", {}) if isinstance(global_config, dict) else {}
        results.append(check("Global MCP config", global_path.exists(), str(global_path)))
        expected = register.expected_servers()
        for name in ("netops_rag", "network_state"):
            actual = servers.get(name, {}) if isinstance(servers, dict) else {}
            results.append(check(f"Global MCP {name} config", bool(actual), str(global_path)))
            configured_python = actual.get("command") if isinstance(actual, dict) else None
            expected_python = expected[name]["command"]
            results.append(check(f"MCP {name} uses current workshop Python", configured_python == expected_python, f"configured={configured_python or 'missing'} expected={expected_python}"))
            tools = actual.get("tools", {}) if isinstance(actual, dict) else {}
            include = set(tools.get("include", []) or []) if isinstance(tools, dict) else set()
            expected_include = set(expected[name]["tools"]["include"])
            results.append(check(f"MCP {name} read-only allowlist", include == expected_include, f"{len(include)}/{len(expected_include)} expected tools"))
    except Exception as exc:
        results.append(check("Global MCP config", False, str(exc)))

    mcp_found = importlib.util.find_spec("mcp") is not None
    mcp_detail = "not installed"
    mcp_v2 = False
    if mcp_found:
        try:
            mcp_version = version("mcp")
            mcp_detail = mcp_version
            mcp_v2 = int(mcp_version.split(".", 1)[0]) == 2
        except (PackageNotFoundError, ValueError):
            mcp_detail = "installed, version unknown"
    results.append(check("MCP SDK v2", mcp_found and mcp_v2, mcp_detail))

    active_path = BONUS / "mock_state" / ".active_scenario"
    active = active_path.read_text(encoding="utf-8").strip() if active_path.exists() else ""
    results.append(check("Active scenario", bool(active) and (BONUS / "mock_state" / active / "scenario.json").exists(), active or "missing"))

    direct = run([sys.executable, str(BONUS / "scripts" / "test_mcp_tools.py")])
    results.append(check("Direct tool smoke test", direct.returncode == 0, f"exit={direct.returncode}"))
    if direct.returncode != 0:
        print(direct.stdout)
        print(direct.stderr)

    if mcp_found:
        protocol = run([sys.executable, str(BONUS / "scripts" / "test_mcp_protocol.py")])
        results.append(check("MCP protocol smoke test", protocol.returncode == 0, f"exit={protocol.returncode}"))
        if protocol.returncode != 0:
            print(protocol.stdout)
            print(protocol.stderr)

    if hermes and not args.skip_hermes_mcp_test:
        for server in ("netops_rag", "network_state"):
            result = run([hermes, "mcp", "test", server], timeout=180)
            output = result.stdout + result.stderr
            ok = result.returncode == 0 and "connected" in output.lower() and "connection failed" not in output.lower()
            detail = "connected" if ok else output.strip()[-700:]
            results.append(check(f"Hermes MCP {server}", ok, detail or f"exit={result.returncode}"))

    if all(results):
        print("\nDesktop bonus preflight passed.")
        print("Launch Desktop, open the NetOps RAG Workshop project, and start a NEW session.")
        print("First prompt: bonus/hermes-netops-copilot/prompts/00-verify-tools.md")
        return

    print("\nRepair command:")
    print(f"  {sys.executable} {BONUS / 'scripts' / 'desktop_profile_setup.py'} --profile {args.profile} --project \"{args.project}\"")
    raise SystemExit("\nDesktop bonus preflight failed. Resolve FAIL items before the live demo.")


if __name__ == "__main__":
    main()
