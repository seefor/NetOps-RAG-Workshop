"""Compatibility wrapper for older bonus instructions.

v8.2 uses desktop_profile_setup.py as the primary path. MCP servers are
registered in Hermes' global MCP registry, while the workshop profile keeps
only its working-directory and skill settings.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

BONUS = Path(__file__).resolve().parents[1]


def load_register_module():
    script = BONUS / "scripts" / "register_global_mcp.py"
    spec = importlib.util.spec_from_file_location("register_global_mcp", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_config(): return load_register_module().expected_servers()


def main() -> None:
    parser = argparse.ArgumentParser(description="Register Hermes NetOps workshop MCP servers")
    parser.add_argument("--apply", action="store_true", help="Kept for compatibility; registration is performed when present")
    parser.add_argument("--replace-existing-mcp", action="store_true")
    parser.add_argument("--skip-test", action="store_true")
    args = parser.parse_args()
    module = load_register_module()
    if not args.apply:
        output = BONUS / "hermes" / "generated-global-mcp-config.yaml"
        import yaml
        output.write_text(yaml.safe_dump({"mcp_servers": module.expected_servers()}, sort_keys=False), encoding="utf-8")
        print(f"Generated reference config: {output}")
        print("v8.2 primary setup: python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py")
        return
    try: path = module.register(replace_existing=args.replace_existing_mcp, test=not args.skip_test)
    except RuntimeError as exc: raise SystemExit(str(exc)) from exc
    print(f"Updated Hermes global MCP config: {path}")


if __name__ == "__main__": main()
