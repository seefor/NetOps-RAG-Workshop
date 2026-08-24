from __future__ import annotations

import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

import yaml


BONUS = Path(__file__).resolve().parents[1]
ROOT = BONUS.parents[1]
SERVER_NAMES = ("netops_rag", "network_state")


def run(cmd: list[str], *, input_text: str | None = None, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, input=input_text, capture_output=True, timeout=timeout)


def workshop_python() -> str:
    return str(Path(sys.executable).absolute())


def expected_servers() -> dict[str, dict[str, Any]]:
    python = workshop_python()
    root = str(ROOT.resolve())
    return {
        "netops_rag": {
            "command": python,
            "args": [str((BONUS / "mcp" / "netops_rag_server.py").resolve())],
            "env": {"NETOPS_WORKSHOP_ROOT": root, "PYTHONPATH": str((ROOT / "src").resolve())},
            "connect_timeout": 30,
            "timeout": 120,
            "enabled": True,
            "tools": {"include": ["search_network_knowledge","retrieve_runbook","retrieve_device_config","retrieve_change_record","retrieve_incident_record","retrieve_postmortem","list_sources"],"prompts": False,"resources": False},
        },
        "network_state": {
            "command": python,
            "args": [str((BONUS / "mcp" / "mock_network_server.py").resolve())],
            "env": {"NETOPS_WORKSHOP_ROOT": root},
            "connect_timeout": 30,
            "timeout": 60,
            "enabled": True,
            "tools": {"include": ["get_scenario_context","list_devices","get_device_facts","get_bgp_summary","get_ipsec_summary","get_interface_status","get_route","get_recent_logs","get_config_diff"],"prompts": False,"resources": False},
        },
    }


def candidate_global_config_paths() -> list[Path]:
    paths=[]
    override=os.getenv("HERMES_HOME")
    if override: paths.append(Path(override).expanduser()/"config.yaml")
    paths.append(Path.home()/".hermes"/"config.yaml")
    out=[]
    for path in paths:
        p=path.absolute()
        if p not in out: out.append(p)
    return out


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def find_actual_global_config() -> Path:
    for path in candidate_global_config_paths():
        data=load_yaml(path); servers=data.get("mcp_servers",{}) if isinstance(data,dict) else {}
        if any(name in servers for name in SERVER_NAMES): return path
    return candidate_global_config_paths()[0]


def backup_config(path: Path) -> Path | None:
    if not path.exists(): return None
    stamp=datetime.now().strftime("%Y%m%d-%H%M%S")
    backup=path.with_name(f"config.yaml.backup-netops-v8.2-{stamp}")
    shutil.copy2(path,backup); return backup


def same_workshop_server(existing: dict[str, Any], expected: dict[str, Any]) -> bool:
    if not isinstance(existing,dict): return False
    existing_args=[str(x) for x in (existing.get("args") or [])]; expected_args=[str(x) for x in (expected.get("args") or [])]
    if not existing_args or not expected_args: return False
    return Path(existing_args[0]).name == Path(expected_args[0]).name and "hermes-netops-copilot" in existing_args[0]


def mcp_add_command(hermes: str, name: str, config: dict[str, Any]) -> list[str]:
    cmd=[hermes,"mcp","add",name,"--command",str(config["command"]),"--connect-timeout",str(config.get("connect_timeout",30))]
    env=config.get("env",{}) or {}
    if env:
        cmd.append("--env"); cmd.extend(f"{key}={value}" for key,value in env.items())
    cmd.append("--args"); cmd.extend(str(arg) for arg in (config.get("args") or []))
    return cmd


def patch_global_filters(path: Path, expected: dict[str, dict[str, Any]]) -> None:
    data=load_yaml(path); data.setdefault("mcp_servers",{})
    for name,wanted in expected.items():
        entry=data["mcp_servers"].setdefault(name,{})
        entry["command"]=wanted["command"]; entry["args"]=wanted["args"]; entry["env"]=wanted["env"]
        entry["enabled"]=True; entry["connect_timeout"]=wanted["connect_timeout"]; entry["timeout"]=wanted["timeout"]; entry["tools"]=wanted["tools"]
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")


def register(*, replace_existing: bool=False, test: bool=True) -> Path:
    hermes=shutil.which("hermes")
    if not hermes: raise RuntimeError("Hermes is not on PATH. Install/open Hermes Desktop first.")
    expected=expected_servers(); global_path=find_actual_global_config(); current=load_yaml(global_path)
    current_servers=current.get("mcp_servers",{}) if isinstance(current,dict) else {}
    for name,wanted in expected.items():
        existing=current_servers.get(name)
        if existing and not same_workshop_server(existing,wanted) and not replace_existing:
            raise RuntimeError(f"Global Hermes MCP server '{name}' already exists and does not look like this workshop. Re-run with --replace-existing-mcp only if you intend to replace it.")
    backup=backup_config(global_path)
    if backup: print(f"Global Hermes config backup: {backup}")
    for name,wanted in expected.items():
        existing=current_servers.get(name); cmd=mcp_add_command(hermes,name,wanted); input_text="y\n\n" if existing else "\n"
        print(f"Registering global MCP server: {name}")
        result=run(cmd,input_text=input_text,timeout=180); output=(result.stdout+result.stderr).strip(); lowered=output.lower()
        if result.returncode != 0 or "server not saved" in lowered or "cancelled" in lowered or "connection failed" in lowered or "failed to connect" in lowered:
            raise RuntimeError(f"Hermes failed to register {name}:\n{output}")
        if output: print(output)
    actual=find_actual_global_config(); patch_global_filters(actual,expected); print(f"Workshop MCP configuration: {actual}")
    if test:
        for name in SERVER_NAMES:
            result=run([hermes,"mcp","test",name],timeout=180); output=(result.stdout+result.stderr).strip()
            ok=result.returncode==0 and "connected" in output.lower() and "connection failed" not in output.lower()
            if not ok: raise RuntimeError(f"Hermes MCP test failed for {name}:\n{output}")
            print(f"MCP test passed: {name}")
    return actual


def main() -> None:
    parser=argparse.ArgumentParser(description="Register the two workshop MCP servers in Hermes global MCP config")
    parser.add_argument("--replace-existing-mcp",action="store_true",help="Replace same-named non-workshop MCP entries if they already exist")
    parser.add_argument("--skip-test",action="store_true"); args=parser.parse_args()
    try: path=register(replace_existing=args.replace_existing_mcp,test=not args.skip_test)
    except RuntimeError as exc: raise SystemExit(str(exc)) from exc
    print("\nGlobal workshop MCP servers are ready."); print("  netops_rag"); print("  network_state"); print(f"Config: {path}")


if __name__ == "__main__": main()
