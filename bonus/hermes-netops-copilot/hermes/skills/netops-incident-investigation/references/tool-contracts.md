# Tool Contracts

## NetOps RAG tools

These return indexed, point-in-time knowledge. Expected Hermes names begin with `mcp_netops_rag_`.

- `search_network_knowledge`
- `retrieve_runbook`
- `retrieve_device_config`
- `retrieve_change_record`
- `retrieve_incident_record`
- `retrieve_postmortem`
- `list_sources`

Do not describe indexed configs as current running configs unless current-state evidence independently establishes that fact.

## Network State tools

These return synthetic current-state evidence. Expected Hermes names begin with `mcp_network_state_`.

- `get_scenario_context`
- `list_devices`
- `get_device_facts`
- `get_bgp_summary`
- `get_ipsec_summary`
- `get_interface_status`
- `get_route`
- `get_recent_logs`
- `get_config_diff`

Every response is synthetic and read-only. Preserve `observed_at` when it matters to the conclusion.

## What does not exist

There are no tools for:

- sending commands
- pushing configuration
- clearing a protocol session
- reloading a device
- approving a change
- modifying the knowledge base

If asked to perform those actions, state the boundary and offer a read-only investigation or change-controlled plan.
