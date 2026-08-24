from __future__ import annotations

import argparse
from datetime import datetime
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

import yaml


BONUS_DIR = Path(__file__).resolve().parents[1]
WORKSHOP_ROOT = BONUS_DIR.parents[1]
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


def build_profile_config() -> dict[str, Any]:
    skill_dir = str((BONUS_DIR / "hermes" / "skills").resolve())
    root = str(WORKSHOP_ROOT.resolve())
    return {
        "terminal": {"cwd": root},
        "skills": {"external_dirs": [skill_dir], "write_approval": True},
    }


def deep_merge_profile(existing: dict[str, Any], addition: dict[str, Any]) -> dict[str, Any]:
    result = dict(existing)
    result.setdefault("terminal", {})
    result["terminal"].update(addition["terminal"])

    result.setdefault("skills", {})
    dirs = list(result["skills"].get("external_dirs", []) or [])
    for path in addition["skills"]["external_dirs"]:
        if path not in dirs:
            dirs.append(path)
    result["skills"]["external_dirs"] = dirs
    result["skills"]["write_approval"] = True

    servers = result.get("mcp_servers")
    if isinstance(servers, dict):
        servers.pop("netops_rag", None)
        servers.pop("network_state", None)
        if not servers:
            result.pop("mcp_servers", None)
    return result


def profile_exists(profile: str) -> bool:
    return profile_home(profile).exists()


def ensure_profile(profile: str, hermes: str, clone: bool) -> None:
    if profile == "default" or profile_exists(profile):
        return
    cmd = [hermes, "profile", "create", profile]
    if clone:
        cmd.append("--clone")
    print(f"Creating Hermes profile: {profile}")
    result = subprocess.run(cmd, cwd=WORKSHOP_ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Could not create Hermes profile {profile}:\n{result.stdout}\n{result.stderr}")


def install_profile_config(profile: str) -> Path:
    home = profile_home(profile)
    home.mkdir(parents=True, exist_ok=True)
    target = home / "config.yaml"
    existing: dict[str, Any] = {}
    if target.exists():
        existing = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = target.with_name(f"config.yaml.backup-netops-v8.2-{stamp}")
        shutil.copy2(target, backup)
        print(f"Profile config backup: {backup}")
    merged = deep_merge_profile(existing, build_profile_config())
    target.write_text(yaml.safe_dump(merged, sort_keys=False), encoding="utf-8")
    return target


def install_soul(profile: str, force: bool = False) -> None:
    source = BONUS_DIR / "hermes" / "SOUL.md"
    target = profile_home(profile) / "SOUL.md"
    if target.exists() and not force:
        print(f"SOUL preserved: {target} already exists (use --force-soul to replace it)")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(target, target.with_name(f"SOUL.md.backup-{stamp}"))
    shutil.copy2(source, target)
    print(f"Installed workshop SOUL: {target}")


def run(cmd: list[str], *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=WORKSHOP_ROOT, text=True, capture_output=True, timeout=timeout)


def ensure_project(profile: str, hermes: str, project_name: str = DEFAULT_PROJECT) -> None:
    root = str(WORKSHOP_ROOT.resolve())
    listing = run([hermes, "-p", profile, "project", "list"])
    list_output = (listing.stdout + listing.stderr).strip()
    if listing.returncode == 0 and project_name.lower() in list_output.lower():
        print(f"Hermes project already registered: {project_name}")
        return

    help_result = run([hermes, "-p", profile, "project", "create", "--help"])
    help_text = help_result.stdout + help_result.stderr
    if "--path" in help_text:
        create_cmd = [hermes, "-p", profile, "project", "create", project_name, "--path", root]
    else:
        create_cmd = [hermes, "-p", profile, "project", "create", project_name, root]

    result = run(create_cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Could not create Hermes project:\n{result.stdout}\n{result.stderr}")
    print(f"Hermes project registered: {project_name} -> {root}")


def load_register_module():
    script = BONUS_DIR / "scripts" / "register_global_mcp.py"
    spec = importlib.util.spec_from_file_location("register_global_mcp", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare Hermes Desktop for the NetOps bonus")
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--no-clone", action="store_true", help="Create a blank profile instead of cloning current provider config")
    parser.add_argument("--force-soul", action="store_true")
    parser.add_argument("--activate", action="store_true", help="Make this the sticky active Hermes profile")
    parser.add_argument("--replace-existing-mcp", action="store_true")
    parser.add_argument("--skip-mcp-test", action="store_true")
    args = parser.parse_args()

    hermes = shutil.which("hermes")
    if not hermes:
        raise SystemExit("Hermes is not on PATH. Install/open Hermes Desktop first, then re-run this script.")

    if not (WORKSHOP_ROOT / "src" / "netops_rag").exists():
        raise SystemExit(f"Workshop root not found: {WORKSHOP_ROOT}")

    try:
        ensure_profile(args.profile, hermes, clone=not args.no_clone)
        target = install_profile_config(args.profile)
        install_soul(args.profile, force=args.force_soul)
        ensure_project(args.profile, hermes, args.project)

        register = load_register_module()
        global_config = register.register(
            replace_existing=args.replace_existing_mcp,
            test=not args.skip_mcp_test,
        )

        if args.activate:
            subprocess.run([hermes, "profile", "use", args.profile], check=True)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc

    generated = BONUS_DIR / "hermes" / "generated-desktop-profile-config.yaml"
    generated.write_text(yaml.safe_dump(build_profile_config(), sort_keys=False), encoding="utf-8")

    print("\nHermes Desktop workshop setup is ready.")
    print(f"Profile: {args.profile}")
    print(f"Project: {args.project}")
    print(f"Profile config: {target}")
    print(f"Global MCP config: {global_config}")
    print("Global MCP servers: netops_rag, network_state")
    print("\nNext:")
    print(f"  {sys.executable} {BONUS_DIR / 'scripts' / 'desktop_preflight.py'} --profile {args.profile} --project \"{args.project}\"")
    print(f"  {sys.executable} {BONUS_DIR / 'scripts' / 'launch_desktop.py'} --profile {args.profile}")


if __name__ == "__main__":
    main()
