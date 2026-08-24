# CLI Fallback Setup — v8.2

Hermes Desktop is the primary bonus surface. The CLI shares the same global MCP registry, profile skills, and scenarios.

From the workshop root with `.venv` active:

```bash
python -m pip install -e ".[hermes]"
netops-rag ingest --data data --reset
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py
python bonus/hermes-netops-copilot/scripts/set_scenario.py bgp-policy-drift
python bonus/hermes-netops-copilot/scripts/desktop_preflight.py
```

Verify the global MCP registry:

```bash
hermes mcp list
hermes mcp test netops_rag
hermes mcp test network_state
```

Then start a CLI session from the workshop root:

```bash
hermes -p netops-workshop --in "$PWD" chat
```

On Windows PowerShell:

```powershell
hermes -p netops-workshop --in "$PWD" chat
```

Paste `prompts/00-verify-tools.md` before the incident prompt.
