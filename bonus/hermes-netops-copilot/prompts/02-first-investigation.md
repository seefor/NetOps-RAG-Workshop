/netops-incident-investigation Investigate the active synthetic incident involving atl-core-r1 and nyc-edge-r1.

Use the already-configured MCP tool namespaces:

- `mcp_netops_rag_*`
- `mcp_network_state_*`

Do not search the MCP catalog, install an MCP server, authorize a new MCP server, or modify MCP configuration. If either namespace is unavailable, stop and report exactly which namespace is missing.

Requirements:

- Use the active approved BGP runbook.
- Review both indexed device snapshots.
- Review CHG-1234 and any relevant incident or postmortem.
- Gather current read-only BGP, interface, route, log, and deterministic config-diff evidence with `mcp_network_state_*` tools.
- Compare documented intent with observed state.
- Do not assume the latest approved change caused the incident merely because it happened recently.
- Do not make changes.
- Produce the incident brief using the skill template.
- Cite retrieved sources and name every MCP tool result used.
