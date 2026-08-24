# NetOps RAG Workshop Stack — Presenter-Ready Four-Hour Edition

> **v8.2 Hermes Desktop baseline:** the bonus now registers `netops_rag` and `network_state` in Hermes' global MCP registry, registers the workshop directory as a Hermes Project, preserves the active `.venv` Python path, and verifies both servers with `hermes mcp test`.

Build a Network Operations RAG assistant that searches a fictional multi-site, multi-vendor environment called **AtlasNet**. The stack is local-first with Ollama and can switch answer generation to OpenAI or Anthropic through environment variables.

## What changed in this edition

- Four labs rewritten to reliably support four-hour delivery
- 40+ synthetic NetOps knowledge files
- Cisco, Juniper, Arista, Palo Alto, and F5 config examples
- BGP, OSPF, switching, DNS, DHCP, IPsec, firewall, load-balancer, platform-health, and incident runbooks
- Approved, completed, scheduled, rejected, retired, decommissioned, lab-only, and untrusted sources
- Metadata filtering from the CLI and Streamlit UI
- Dataset statistics and catalog commands
- Incident, postmortem, and source-of-truth examples
- Stale-document and prompt-injection exercises
- Scenario cards and instructor answer key
- Expanded evaluation questions
- Runbook-aligned 44-slide presenter script with timing, talk tracks, audience questions, demo cues, and transitions

## Architecture

```text
Runbooks / configs / policies / changes / incidents / inventory
        ↓
Paragraph-aware chunking + metadata
        ↓
Embeddings: Ollama or OpenAI
        ↓
Chroma persistent vector store
        ↓
Semantic retrieval + metadata filters
        ↓
Generation: Ollama, OpenAI, or Anthropic
        ↓
NetOps answer with citations and guardrails
```

## Quick start with Ollama

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
ollama pull llama3.2
ollama pull embeddinggemma
python scripts/preflight.py
netops-rag stats --data data
netops-rag ingest --data data --reset
netops-rag ask "Why did the BGP session between atl-core-r1 and nyc-edge-r1 flap?"
python -m streamlit run streamlit_app.py
```

## Provider switching

### Ollama

```env
LLM_PROVIDER=ollama
EMBEDDINGS_PROVIDER=ollama
OLLAMA_CHAT_MODEL=llama3.2
OLLAMA_EMBED_MODEL=embeddinggemma
```

### OpenAI

```env
LLM_PROVIDER=openai
EMBEDDINGS_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_CHAT_MODEL=gpt-5-mini
OPENAI_EMBED_MODEL=text-embedding-3-small
```

Reset and re-ingest when changing the embedding provider or model. If you are upgrading from a pre-v0.5.0 workshop zip, reset/re-ingest once so the collection records its embedding provider/model.

### Anthropic answer generation with local embeddings

```env
LLM_PROVIDER=anthropic
EMBEDDINGS_PROVIDER=ollama
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-sonnet-5
```

## New CLI commands

```bash
netops-rag stats --data data
netops-rag catalog --data data --doc-type config
netops-rag retrieve "BGP down" --status active --service bgp --top-k 5
netops-rag ask "Compare the two trunk uplinks" --device atl-access-sw1 --device atl-dist-sw1
```

Repeat the same filter flag to create an OR match within that field. Different filter fields are combined with AND.

## Instructor helper commands

Run the environment preflight before the workshop:

```bash
python scripts/preflight.py
```

Switch answer providers without manually rewriting `.env`:

```bash
python scripts/set_provider.py ollama
python scripts/set_provider.py openai
python scripts/set_provider.py anthropic
```

Use `instructor/PRESENTER_SCRIPT.md` for what to present and say, and `instructor/DEMO_SCRIPT.md` for the exact command-by-command delivery flow.

## Workshop files

- `WORKSHOP.md` — four-hour run of show
- `labs/` — expanded student labs
- `instructor/PRESENTER_SCRIPT.md` — authoritative slide-by-slide presenter narrative, timing, questions, demo cues, and transitions
- `instructor/TALKING_POINTS.md` — pointer to the current presenter materials
- `instructor/DEMO_SCRIPT.md` — exact instructor command runbook, expected results, teaching cues, and recovery path
- `instructor/SCENARIO_ANSWER_KEY.md` — scenario debrief answers
- `slides/SLIDE_STORYBOARD.md` — slide-by-slide foundation
- `scenarios/SCENARIO_CARDS.md` — group and capstone exercises
- `DATASET_GUIDE.md` — source taxonomy and intended traps

## Important boundary

RAG is useful for finding, correlating, explaining, and citing operational knowledge. It is not a deterministic configuration parser, live-state collector, authorization system, or change executor. Pair it with NetBox, pyATS, Batfish, NAPALM, vendor APIs, authenticated tools, change control, and human approval for production use.


## Optional Hermes Agent bonus

The `bonus/hermes-netops-copilot/` module turns the workshop RAG stack into a governed incident copilot. It adds two read-only MCP servers, synthetic BGP and IPsec state, a reusable Hermes skill, exact instructor commands, prompt files, tests, and expected outputs.

```bash
python -m pip install -e ".[hermes]"
# Keep .venv activated: the global MCP registrations must use this exact Python.
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py
python bonus/hermes-netops-copilot/scripts/desktop_preflight.py
python bonus/hermes-netops-copilot/scripts/launch_desktop.py
```

The bonus is now **Hermes Desktop-first** on macOS, Linux, and Windows, with an isolated `netops-workshop` profile. Use `bonus/hermes-netops-copilot/BONUS_DEMO_RUNBOOK.md` for the 15-minute closing demonstration. The bonus keeps the core boundary intact: RAG supplies trusted knowledge, read-only tools supply observed state, Hermes orchestrates the workflow, and a human owns production approval.
