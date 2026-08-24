# Bonus File Manifest

## Primary Desktop path

- `README.md`
- `HERMES_SETUP.md`
- `CROSS_PLATFORM_DESKTOP.md`
- `BONUS_DEMO_RUNBOOK.md`
- `DESKTOP_PRESENTER_NOTES.md`
- `BONUS_PRESENTER_NOTES.md`
- `ARCHITECTURE.md`
- `SECURITY.md`
- `TROUBLESHOOTING.md`
- `scripts/desktop_profile_setup.py`
- `scripts/desktop_preflight.py`
- `scripts/launch_desktop.py`
- `scripts/install_bonus.sh`
- `scripts/install_bonus.ps1`

## CLI fallback

- `CLI_FALLBACK_SETUP.md`
- `CLI_FALLBACK_DEMO_RUNBOOK.md`
- `scripts/configure_hermes.py` (compatibility wrapper)
- `scripts/register_global_mcp.py` — registers and validates the two workshop MCP servers in Hermes global MCP config
- `scripts/preflight.py`

## Agent assets

- `AGENTS.md`
- `hermes/SOUL.md`
- `hermes/config.example.yaml`
- `hermes/skills/netops-incident-investigation/SKILL.md`
- `hermes/skills/netops-incident-investigation/references/source-authority.md`
- `hermes/skills/netops-incident-investigation/references/tool-contracts.md`
- `hermes/skills/netops-incident-investigation/templates/incident-report.md`

## MCP servers

- `mcp/__init__.py`
- `mcp/bootstrap.py`
- `mcp/knowledge_tools.py`
- `mcp/mock_network_server.py`
- `mcp/netops_rag_server.py`
- `mcp/network_state_tools.py`

## Scenarios and prompts

- `mock_state/.active_scenario`
- `mock_state/bgp-policy-drift/scenario.json`
- `mock_state/branch-ipsec/scenario.json`
- `prompts/00-verify-tools.md`
- `prompts/01-knowledge-only.md`
- `prompts/02-first-investigation.md`
- `prompts/03-second-investigation.md`
- `prompts/04-guardrail-test.md`
- `prompts/05-propose-skill-improvement.md`
- `expected_outputs/first-investigation.md`

## Validation

- `scripts/set_scenario.py`
- `scripts/test_mcp_protocol.py`
- `scripts/test_mcp_tools.py`
- `tests/test_configure_hermes.py`
- `tests/test_desktop_profile_setup.py`
- `tests/test_knowledge_tools.py`
- `tests/test_mock_tools.py`
- `requirements.txt`
