from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess

BONUS=Path(__file__).resolve().parents[1]; ROOT=BONUS.parents[1]; DEFAULT_PROFILE="netops-workshop"

def main() -> None:
    parser=argparse.ArgumentParser(description="Launch Hermes Desktop into the NetOps workshop"); parser.add_argument("--profile",default=DEFAULT_PROFILE); args=parser.parse_args()
    hermes=shutil.which("hermes")
    if not hermes: raise SystemExit("Hermes is not on PATH. Install Hermes Desktop/Agent first.")
    print(f"Launching Hermes Desktop profile '{args.profile}' with workspace: {ROOT}")
    print("In Desktop, open the registered 'NetOps RAG Workshop' project and start a NEW session.")
    subprocess.Popen([hermes,"-p",args.profile,"desktop","--cwd",str(ROOT)])

if __name__ == "__main__": main()
