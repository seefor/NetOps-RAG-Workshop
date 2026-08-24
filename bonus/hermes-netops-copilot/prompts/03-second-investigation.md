/netops-incident-investigation Investigate the active synthetic branch IPsec incident.

Use only the already-configured `mcp_netops_rag_*` and `mcp_network_state_*` namespaces. Do not search the MCP catalog, install an MCP server, or change MCP configuration. If either namespace is missing, stop and report the missing namespace.

Users at branch-01 cannot reach Atlanta applications. The WAN is reported up.

Use the same governed investigation procedure:

- Retrieve the active IPsec runbook and relevant branch configuration.
- Gather current read-only device facts, IPsec state, interface state, route, logs, and config-diff evidence from both ends.
- Separate documented intent from observed state.
- Identify the likely cause and confidence.
- Do not reset the tunnel or make a change.
- State the approval and rollback considerations for remediation.
- Produce the standard incident brief.
- Name every MCP tool result used.
