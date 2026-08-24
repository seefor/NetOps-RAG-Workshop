# Bonus Demo Runbook — Hermes Desktop NetOps Incident Copilot

Use this as the exact 15-minute presenter flow after the core RAG workshop.

## Before you start

From the workshop root:

```bash
source .venv/bin/activate
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py
python bonus/hermes-netops-copilot/scripts/set_scenario.py bgp-policy-drift
python bonus/hermes-netops-copilot/scripts/desktop_preflight.py
python bonus/hermes-netops-copilot/scripts/launch_desktop.py
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python bonus\hermes-netops-copilot\scripts\desktop_profile_setup.py
python bonus\hermes-netops-copilot\scripts\set_scenario.py bgp-policy-drift
python bonus\hermes-netops-copilot\scripts\desktop_preflight.py
python bonus\hermes-netops-copilot\scripts\launch_desktop.py
```

Do not start the demo until `desktop_preflight.py` says the Desktop bonus preflight passed.

## 0:00–0:02 — Frame the transition

> Everything we built today was the knowledge layer. Now we will let an agent decide which approved knowledge and read-only evidence it needs next.

## 0:02–0:04 — Verify capability surface

Paste `prompts/00-verify-tools.md`.

Expected namespaces:

```text
mcp_netops_rag_*
mcp_network_state_*
```

If either namespace is absent, stop. Do not let Hermes search the MCP catalog. Exit Desktop, run `desktop_profile_setup.py`, run `desktop_preflight.py`, then start a new Desktop session.

Teaching point:

> We did not give the agent a configure tool and ask it not to use it. The mutation capability is absent.

## 0:04–0:06 — RAG-only investigation

Paste `prompts/01-knowledge-only.md`.

Ask the room what is still missing:

- current BGP state
- interface state
- route to the peer
- current logs
- current config drift

Transition:

> Indexed knowledge tells us where to look. It does not prove what the network is doing now.

## 0:06–0:11 — Full incident investigation

Paste `prompts/02-first-investigation.md`.

Watch the live tool activity. The expected evidence chain is:

1. `mcp_netops_rag_retrieve_runbook`
2. `mcp_netops_rag_retrieve_device_config` for both devices
3. change / incident / postmortem retrieval
4. `mcp_network_state_get_bgp_summary`
5. `mcp_network_state_get_interface_status`
6. `mcp_network_state_get_route`
7. `mcp_network_state_get_recent_logs`
8. `mcp_network_state_get_config_diff`

Expected conclusion:

- Underlay reachability is available.
- BGP is failing.
- Junos import-policy evaluation is failing.
- Deterministic diff shows unapproved policy drift on `nyc-edge-r1`.
- CHG-1234 should not be blamed merely because it happened recently.

Say:

> Watch the evidence chain, not the prose. RAG supplied the approved procedure and history. Read-only tools supplied current state and deterministic drift. Hermes correlated those facts.

## 0:11–0:14 — Reuse the skill

Switch the scenario:

```bash
python bonus/hermes-netops-copilot/scripts/set_scenario.py branch-ipsec
```

Paste `prompts/03-second-investigation.md`.

Expected evidence:

- WAN interface up
- route to VPN peer present
- IKE authentication failing
- branch identity certificate expired
- no config drift

Show the `netops-incident-investigation` skill.

Say:

> The reusable asset is not the BGP answer. It is the investigation discipline: scope, retrieve, observe, compare, disclose uncertainty, and recommend a safe next step.

## 0:14–0:15 — Close

> RAG gives the agent trusted knowledge. MCP gives it controlled evidence. Skills give it repeatable operational discipline. The engineer remains in control of production.

## Fallback

If Desktop has a UI issue, use `CLI_FALLBACK_DEMO_RUNBOOK.md`. If MCP namespaces are missing, fix MCP registration first; never let the agent substitute a public catalog server.
