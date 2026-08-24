# Troubleshooting — Hermes Desktop Bonus

## Hermes says `No MCP servers configured`

In v8.2, run:

```bash
python bonus/hermes-netops-copilot/scripts/register_global_mcp.py
hermes mcp list
```

The workshop servers should appear as:

```text
netops_rag
network_state
```

## Hermes says `netops-rag is not in the MCP catalog`

That means the session did not have the workshop MCP namespaces loaded and attempted catalog discovery. Stop the incident.

The workshop servers are local custom servers, not catalog entries. Run:

```bash
hermes mcp list
hermes mcp test netops_rag
hermes mcp test network_state
```

Then fully quit Desktop, relaunch it, and create a new session. The model-visible namespaces should begin with:

```text
mcp_netops_rag_
mcp_network_state_
```

## MCP test says `Connection closed`

Check that the configured command is the workshop virtual-environment Python, not Homebrew/system Python.

```bash
python -c "import sys; print(sys.executable)"
hermes mcp list
```

If the stored command is wrong, rerun:

```bash
python bonus/hermes-netops-copilot/scripts/register_global_mcp.py --replace-existing
```

## Desktop project is missing

Run:

```bash
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py
hermes -p netops-workshop project list
```

You should see **NetOps RAG Workshop** pointing at the workshop root.

## Desktop shows the project but no sessions

That is normal on first use. Create a new session after MCP registration succeeds. If the Desktop UI cannot create one, use the CLI fallback from the workshop root:

```bash
hermes -p netops-workshop --in "$PWD" chat
```

## Protocol smoke test raises `tuple has no attribute name`

You are using the v8 smoke-test script against MCP SDK v2. v8.2 uses `ListToolsResult.tools`. Use the current v8.2 package.

## Ollama connection refused

The RAG MCP server requires the configured embedding provider. If `.env` uses Ollama embeddings, make sure Ollama is running and `embeddinggemma` exists.

## Agent tries to use non-workshop MCP tools

Use the workshop prompt files exactly. They name the required namespaces and explicitly prohibit installing or substituting catalog MCP servers.

## Remote gateway is selected

Local stdio servers cannot be launched on your laptop by a remote Hermes backend. Select the Local gateway for the workshop bonus.
