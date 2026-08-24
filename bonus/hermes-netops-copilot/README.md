# Bonus — Hermes Desktop NetOps Incident Copilot

This optional 15-minute workshop finale turns the NetOps RAG knowledge layer into a governed incident-investigation agent in Hermes Desktop.

## v8.2 quick start

From the workshop root with `.venv` active:

```bash
python -m pip install -e ".[hermes]"
netops-rag ingest --data data --reset
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py
python bonus/hermes-netops-copilot/scripts/set_scenario.py bgp-policy-drift
python bonus/hermes-netops-copilot/scripts/desktop_preflight.py
python bonus/hermes-netops-copilot/scripts/launch_desktop.py
```

Then open the **NetOps RAG Workshop** project in Desktop, start a new session, and paste `prompts/00-verify-tools.md`.

Expected tool namespaces:

```text
mcp_netops_rag_*
mcp_network_state_*
```

The workshop MCP servers are local custom stdio servers. They are **not** entries in the Hermes MCP catalog. The prompts and skill explicitly prohibit catalog installation during an incident.

## What v8.2 fixes

- registers MCP servers in the Hermes global MCP registry instead of the workshop profile
- validates the registry with the real `hermes mcp list/test` commands
- registers the workshop folder as a Hermes Project
- preserves the exact `.venv` Python executable
- keeps read-only MCP tool allowlists
- updates prompts and the skill to use exact MCP namespaces
- prevents the agent from trying to install a similarly named catalog MCP

See `HERMES_SETUP.md` and `BONUS_DEMO_RUNBOOK.md`.
