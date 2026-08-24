from __future__ import annotations

from pathlib import Path
import importlib.util
from importlib.metadata import PackageNotFoundError, version
import os
import shutil
import subprocess
import sys


BONUS = Path(__file__).resolve().parents[1]
ROOT = BONUS.parents[1]


def check(label: str, ok: bool, detail: str) -> bool:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {label}: {detail}")
    return ok


def main() -> None:
    results = []
    results.append(check("Python", sys.version_info >= (3, 10), sys.version.split()[0]))
    results.append(check("Workshop root", (ROOT / "src/netops_rag").exists(), str(ROOT)))
    results.append(check("Workshop .env", (ROOT / ".env").exists(), str(ROOT / ".env")))
    mcp_found = importlib.util.find_spec("mcp") is not None
    mcp_detail = "not installed"
    mcp_v2 = False
    if mcp_found:
        try:
            mcp_version = version("mcp")
            mcp_detail = mcp_version
            major = int(mcp_version.split(".", 1)[0])
            mcp_v2 = major == 2
        except (PackageNotFoundError, ValueError):
            mcp_detail = "installed, version unknown"
    results.append(check("MCP SDK v2", mcp_found and mcp_v2, mcp_detail))
    results.append(check("PyYAML", importlib.util.find_spec("yaml") is not None, "required by config generator"))
    results.append(check("Hermes CLI", shutil.which("hermes") is not None, shutil.which("hermes") or "not on PATH"))
    results.append(check("RAG server", (BONUS / "mcp/netops_rag_server.py").exists(), "present"))
    results.append(check("State server", (BONUS / "mcp/mock_network_server.py").exists(), "present"))
    results.append(check("Skill", (BONUS / "hermes/skills/netops-incident-investigation/SKILL.md").exists(), "present"))
    active = (BONUS / "mock_state/.active_scenario").read_text(encoding="utf-8").strip()
    results.append(check("Active scenario", (BONUS / "mock_state" / active / "scenario.json").exists(), active))

    print("\nDirect tool smoke test:")
    completed = subprocess.run([sys.executable, str(BONUS / "scripts/test_mcp_tools.py")], cwd=ROOT, text=True, capture_output=True)
    print(completed.stdout.strip())
    if completed.stderr.strip(): print(completed.stderr.strip())
    results.append(check("Direct tool smoke test", completed.returncode == 0, f"exit={completed.returncode}"))

    if importlib.util.find_spec("mcp") is not None:
        protocol = subprocess.run([sys.executable, str(BONUS / "scripts/test_mcp_protocol.py")], cwd=ROOT, text=True, capture_output=True)
        print("\nMCP protocol smoke test:")
        print(protocol.stdout.strip())
        if protocol.stderr.strip(): print(protocol.stderr.strip())
        results.append(check("MCP protocol smoke test", protocol.returncode == 0, f"exit={protocol.returncode}"))

    if all(results):
        print("\nBonus preflight passed.")
        return
    raise SystemExit("\nBonus preflight failed. Resolve FAIL items before the live demo.")


if __name__ == "__main__": main()
