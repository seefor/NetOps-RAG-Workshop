#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -e ".[hermes]"
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py
python bonus/hermes-netops-copilot/scripts/desktop_preflight.py

echo
echo "Desktop bonus is configured. Launch with:"
echo "python bonus/hermes-netops-copilot/scripts/launch_desktop.py"
