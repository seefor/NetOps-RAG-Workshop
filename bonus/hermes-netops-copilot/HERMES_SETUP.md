# Hermes Desktop Setup — NetOps Incident Copilot Bonus (v8.2)

This is the primary setup path for the optional Hermes Desktop bonus on macOS, Linux, or Windows.

## v8.2 configuration model

Hermes Desktop uses two different configuration scopes in this workshop:

```text
Hermes profile: netops-workshop
  ├─ working directory
  ├─ external skill directory
  └─ skill-write approval

Hermes global MCP registry
  ├─ netops_rag
  └─ network_state

Hermes Project
  └─ NetOps RAG Workshop -> this repository root
```

The two local MCP servers are **not MCP catalog entries**. They are custom local stdio servers registered by the workshop setup script.

> Use the **Local** Hermes gateway for the bonus. Local stdio servers must run on the same host as the Hermes backend.

## 1. Prepare the workshop environment

From the repository root:

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[hermes]"
cp .env.example .env   # only if .env does not exist
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[hermes]"
Copy-Item .env.example .env   # only if .env does not exist
```

Keep the workshop virtual environment active. The MCP subprocesses must use this exact Python executable.

For the Ollama-first workshop:

```bash
ollama pull embeddinggemma
ollama pull llama3.2
netops-rag ingest --data data --reset
```

## 2. Run the one-step Hermes Desktop setup

```bash
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py
```

The script will:

1. Create or reuse the `netops-workshop` Hermes profile.
2. Put the workshop working directory and external skill directory in the profile config.
3. Remove stale v8/v8.1 workshop MCP entries from the profile config.
4. Register `netops_rag` and `network_state` through Hermes' global MCP registry.
5. Preserve the exact active `.venv` Python path for both stdio servers.
6. Apply read-only tool allowlists to both servers.
7. Register or reuse the **NetOps RAG Workshop** Hermes Project for this folder.
8. Back up Hermes configuration before changing it.
9. Test both MCP servers through the actual Hermes CLI.

If same-named non-workshop MCP servers already exist, setup stops instead of overwriting them. Only use this if you intentionally want to replace them:

```bash
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py --replace-existing-mcp
```

## 3. Validate everything

```bash
python bonus/hermes-netops-copilot/scripts/desktop_preflight.py
```

A clean run verifies:

- profile config and working directory
- registered Hermes Project
- global MCP registry contains both workshop servers
- both servers use the active workshop `.venv` Python
- read-only tool allowlists
- MCP SDK v2 protocol
- direct tool smoke tests
- actual `hermes mcp test` connectivity
- active synthetic scenario

## 4. Launch Desktop

```bash
python bonus/hermes-netops-copilot/scripts/launch_desktop.py
```

In Desktop:

1. Open **NetOps RAG Workshop** in the Projects sidebar.
2. Start a **new session** after MCP configuration changes.
3. Confirm the **Local** gateway.
4. Paste `prompts/00-verify-tools.md` first.

Expected MCP namespaces:

```text
mcp_netops_rag_*
mcp_network_state_*
```

The verification prompt explicitly tells Hermes **not** to search the MCP catalog or install anything. If either namespace is missing, fix configuration before running the incident demo.

## 5. Prepare the first scenario

```bash
python bonus/hermes-netops-copilot/scripts/set_scenario.py bgp-policy-drift
```

Then follow `BONUS_DEMO_RUNBOOK.md`.

## Manual repair commands

If you only need to repair MCP registration:

```bash
python bonus/hermes-netops-copilot/scripts/register_global_mcp.py
```

Then verify with Hermes itself:

```bash
hermes mcp list
hermes mcp test netops_rag
hermes mcp test network_state
```

Do **not** add `-p netops-workshop` to these MCP commands in this workshop build; the tested Hermes MCP registry is global.

## Provider note

Hermes Desktop controls the agent inference model. The RAG MCP server uses the workshop `.env` for embeddings. They do not have to use the same provider.
