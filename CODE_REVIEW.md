# Code Review — v8.2 Baseline

## Scope

This review incorporates issues discovered during live Mac validation of the Streamlit and Hermes Desktop paths.

## Resolved issues

1. Streamlit package-relative import failure — fixed with a root `streamlit_app.py` entrypoint and absolute package imports.
2. Chroma reset on a nonexistent collection — reset is idempotent across `NotFoundError` / legacy `ValueError` behavior.
3. Embedding-provider/model mismatch — collection metadata now produces an explicit rebuild message.
4. MCP SDK v2 `list_tools()` response shape — protocol smoke test reads `ListToolsResult.tools`.
5. Virtual-environment Python symlink resolution — MCP subprocesses preserve the exact active `.venv` interpreter.
6. Hermes Desktop Project registration — setup registers **NetOps RAG Workshop** and handles tested path-syntax variants.
7. Hermes MCP scope mismatch — workshop servers are now registered through Hermes' global MCP registry rather than profile config.
8. Preflight false positive — preflight now validates the real `hermes mcp list/test` results instead of only inspecting a generated profile YAML file.
9. MCP catalog confusion — prompts and the reusable skill require exact `mcp_netops_rag_*` and `mcp_network_state_*` namespaces and explicitly forbid catalog installation during an incident.
10. Safety surface — global MCP config is patched with explicit read-only tool allowlists after registration.

## v8.2 configuration contract

```text
Profile: netops-workshop
  -> cwd, skills, skill-write approval

Project: NetOps RAG Workshop
  -> workshop repository path

Global MCP registry
  -> netops_rag
  -> network_state
```

## Remaining limitations

The live Hermes Desktop UI can change between releases. The package therefore includes CLI fallbacks and direct `hermes mcp test` verification so the bonus does not depend on a single GUI path.
