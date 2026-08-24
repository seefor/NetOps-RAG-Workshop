# CLI Fallback Demo Runbook — v8.2

Use this only if Hermes Desktop has a UI problem.

```bash
source .venv/bin/activate
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py
python bonus/hermes-netops-copilot/scripts/set_scenario.py bgp-policy-drift
python bonus/hermes-netops-copilot/scripts/desktop_preflight.py
hermes -p netops-workshop --in "$PWD" chat
```

In the Hermes chat, paste in this order:

1. `prompts/00-verify-tools.md`
2. `prompts/01-knowledge-only.md`
3. `prompts/02-first-investigation.md`

For the second incident, switch scenario in another terminal:

```bash
python bonus/hermes-netops-copilot/scripts/set_scenario.py branch-ipsec
```

Then paste `prompts/03-second-investigation.md`.

If either `mcp_netops_rag_*` or `mcp_network_state_*` is missing, stop. Do not allow Hermes to install a similarly named server from the MCP catalog.
