# NetOps RAG Workshop — Runbook-Aligned Slide Storyboard

This storyboard is derived from `instructor/DEMO_SCRIPT.md` and pairs with `instructor/PRESENTER_SCRIPT.md`.

| # | Slide title | Core visual | Demo runbook cue |
|---:|---|---|---|
| 1 | RAG for Network Operations | Knowledge sources → cited answer | — |
| 2 | The workshop promise | One large outcome statement | — |
| 3 | What you will build | Four lab blocks | — |
| 4 | The safety boundary | Assist vs authorize/execute | Sections 1–3 ready |
| 5 | Meet AtlasNet | Synthetic topology and source types | — |
| 6 | The NetOps knowledge problem | Distributed operational knowledge | — |
| 7 | Networking knowledge is not environment knowledge | Generic model vs local evidence | — |
| 8 | Opening demo: generic answer vs local evidence | AtlasNet BGP question | Step 4.1 |
| 9 | RAG in one sentence | Retrieve, then generate | — |
| 10 | The workshop stack | Full RAG architecture | — |
| 11 | Ollama first, cloud optional | Provider adapter | — |
| 12 | Relevant is not authoritative | Source-authority ladder | — |
| 13 | Lab 1 mission | Retrieval controls | — |
| 14 | What is in the knowledge base? | Document categories | Steps 5.1–5.2 |
| 15 | Ingestion creates searchable evidence | Ingestion pipeline | Step 5.3 |
| 16 | Retrieval is a relevance hypothesis | Mixed source cards | Step 5.4 |
| 17 | Top-K controls evidence volume | K=3 vs K=10 | Step 5.5 |
| 18 | Metadata scopes retrieval | Filter funnel | Step 5.6 |
| 19 | Anatomy of a grounded answer | Facts, validation, safety, citations | Step 5.7 |
| 20 | Know when evidence is insufficient | No-live-telemetry boundary | Step 5.8 |
| 21 | Lab 2 mission | Multi-vendor evidence | — |
| 22 | One knowledge layer, multiple vendors | Vendor configs + shared metadata | Step 6.1 |
| 23 | Read the source first | Highlighted Atlanta config | Step 6.2 |
| 24 | Scope retrieval to one device | Device-filtered query | Steps 6.3–6.4 |
| 25 | Explain with RAG; validate with tools | Two-lane boundary | — |
| 26 | Cross-vendor evidence discovery | Cisco and Juniper comparison | Step 6.5 |
| 27 | Find the VLAN mismatch | Side-by-side trunks + incident | Steps 6.6–6.7 |
| 28 | Lab 3 mission | Multi-source evidence board | — |
| 29 | Investigations need an evidence chain | Six source types | Step 7.1 |
| 30 | Retrieve before generating | Evidence list only | Step 7.2 |
| 31 | Build the timeline | Five-event timeline | — |
| 32 | Ask for facts, hypotheses, conflicts, validation | Structured prompt | Step 7.3 |
| 33 | RAG does not prove causality alone | Evidence → synthesis → validation | — |
| 34 | Approved intent vs observed implementation | Firewall change vs config | Steps 7.4–7.5 |
| 35 | Lab 4 mission | Guardrail shield | — |
| 36 | Similarity can retrieve dangerous content | Active, retired, untrusted sources | Steps 8.1–8.2 |
| 37 | Retrieved instructions are data | Prompt-injection containment | Step 8.3 |
| 38 | Safe assistance stops before action | Unsafe prompts + safe response | Step 8.4 |
| 39 | Evaluation is a behavior regression test | Evaluation dimensions | Step 8.5 |
| 40 | Put the workflow behind an interface | Streamlit UI | Section 9 |
| 41 | Switch answer models, keep the stack | Ollama/OpenAI/Anthropic | Section 10 |
| 42 | What production adds | Workshop-to-production architecture | — |
| 43 | The operating model | Knowledge, retrieval, validation, control | — |
| 44 | Final takeaway | RAG is the knowledge layer | Section 12 |

## Slide construction rule

Each slide should communicate one concept. Put detailed narration in presenter notes, not on the slide. Use the terminal for exact commands and source inspection.


## Optional Bonus Slides — Hermes NetOps Incident Copilot

1. We Built the Knowledge Layer
2. Intent Is Not Operational State
3. Add a Governed Agent
4. Safety Is a Tool-Surface Decision
5. Evidence Before Recommendation
6. A Skill, Not a One-Off Answer

Detailed talk track: `bonus/hermes-netops-copilot/BONUS_PRESENTER_NOTES.md`.
