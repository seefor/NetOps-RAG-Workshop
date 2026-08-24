# Hermes NetOps Incident Copilot Architecture — v8.2

```text
                    Hermes Desktop
                         │
                 netops-workshop profile
                         │
                    Hermes Agent
              ┌──────────┴──────────┐
              │                     │
          NetOps RAG MCP       Network State MCP
              │                     │
     trusted indexed docs      synthetic read-only state
              │                     │
              └──────────┬──────────┘
                         │
             netops-incident-investigation
                         │
               evidence-backed brief
```

## Configuration scope

Hermes MCP servers are registered in the global Hermes MCP registry in the tested Desktop build. The `netops-workshop` profile isolates the workshop working directory, skills, and profile-level settings, but should not be treated as the owner of MCP registration.

## Knowledge tools

Expected model-visible names begin with `mcp_netops_rag_`.

- `search_network_knowledge`
- `retrieve_runbook`
- `retrieve_device_config`
- `retrieve_change_record`
- `retrieve_incident_record`
- `retrieve_postmortem`
- `list_sources`

## State tools

Expected model-visible names begin with `mcp_network_state_`.

- `get_scenario_context`
- `list_devices`
- `get_device_facts`
- `get_bgp_summary`
- `get_ipsec_summary`
- `get_interface_status`
- `get_route`
- `get_recent_logs`
- `get_config_diff`

## Safety model

There is intentionally no mutation tool. The agent cannot configure devices, clear sessions, reload devices, or approve changes through the workshop MCP surface.
