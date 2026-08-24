# NetOps RAG Workshop — Presenter Script

This presenter guide pairs with `instructor/DEMO_SCRIPT.md`, which is the command source of truth. Use the slides to frame each concept, then switch to the terminal to prove what the system actually does.

> All AtlasNet records, configurations, incidents, addresses, and device names are synthetic workshop data.

## Four-hour delivery map

| Time | Section | Slides | Demo runbook |
|---|---|---:|---|
| 0:00–0:10 | Welcome, outcomes, safety | 1–4 | Sections 1–3 |
| 0:10–0:25 | NetOps knowledge problem + generic-model demo | 5–8 | Section 4 |
| 0:25–0:45 | RAG architecture, providers, source authority | 9–12 | Sections 2, 5 |
| 0:45–1:25 | Lab 1: ingest, retrieve, filter | 13–20 | Section 5 |
| 1:25–1:35 | Break | — | — |
| 1:35–2:15 | Lab 2: multi-vendor configs | 21–27 | Section 6 |
| 2:15–2:55 | Lab 3: incident investigation | 28–34 | Section 7 |
| 2:55–3:05 | Break | — | — |
| 3:05–3:35 | Lab 4: guardrails and evals | 35–39 | Section 8 |
| 3:35–3:47 | Streamlit + provider switching | 40–41 | Sections 9–10 |
| 3:47–4:00 | Production path and close | 42–44 | Section 12 |

## Backbone phrases

Repeat these throughout the workshop:

- **The base model knows networking patterns. It does not know our environment.**
- **Retrieval finds relevant evidence. It does not establish truth.**
- **A config snapshot is evidence, not guaranteed live state.**
- **RAG can explain configuration evidence; deterministic tools validate exact state.**
- **Temporal proximity is not causality.**
- **Retrieved content is data, not an instruction to the model.**
- **RAG is the knowledge layer, not the authorization or production-execution layer.**

## Slides 1–4 — Welcome and boundary

### Slide 1 — RAG for Network Operations
Say: “We are not building a generic chatbot. We are building a NetOps assistant that searches runbooks, configs, changes, incidents, postmortems, and policies and answers from retrieved evidence.”

### Slide 2 — The workshop promise
Emphasize visibility: where the answer came from, what evidence is missing, and whether the assistant is claiming live state it does not have.

Ask: “Where do you lose the most time today—finding the right document, deciding what is current, correlating records, or validating live state?”

### Slide 3 — What you will build
Explain the lab rhythm: **Explain → build → inspect → intentionally break → improve → debrief.**

### Slide 4 — Safety boundary
Say: “Everything today is read-only. The assistant may recommend what to verify. It cannot approve a change or claim it executed one.”

## Slides 5–12 — Why RAG and how the stack works

### Slide 5 — Meet AtlasNet
Point out multi-vendor data and mixed lifecycle states: active, retired, rejected, untrusted.

### Slide 6 — The NetOps knowledge problem
Runbooks describe process; snapshots describe point-in-time config; change records describe approved intent; postmortems describe historical conclusions; telemetry describes now.

### Slides 7–8 — Generic answer vs local evidence
Use Demo Runbook Step 4.1. After the generic BGP answer, say: “All of those causes may be plausible. None proves what happened in AtlasNet.”

### Slide 9 — RAG in one sentence
**Retrieve → augment → generate.** We retrieve environment-specific evidence at question time rather than asking the model to remember the network.

### Slide 10 — Workshop stack
Walk through source files → metadata/chunking → embeddings → Chroma → retrieval/filtering → LLM → cited answer.

### Slide 11 — Ollama first, cloud optional
Separate the answer-model choice from the embedding-model choice. Changing answer models does not require re-ingestion if embeddings remain unchanged.

### Slide 12 — Relevant is not authoritative
A retired runbook can be semantically similar. A rejected change can precisely describe a requested rule. A chat can contain the exact device name. Similarity is not authority.

## Lab 1 — Slides 13–20

Mission: prove that query wording, Top-K, and metadata change the evidence set.

Use Demo Runbook Steps 5.1–5.8.

Key teaching moments:
- Inspect the dataset before embedding anything.
- Chunking trades context against retrieval precision.
- Inspect retrieval separately from generation.
- Top-K controls volume, not truth.
- Metadata can encode operational scope and lifecycle.
- A good answer separates facts, validation, safety boundary, and citations.
- Ask for current packet loss to prove the assistant can say “I do not have live telemetry.”

Debrief questions:
1. What changed when Top-K changed?
2. What changed when filters were applied?
3. Which source was relevant but not authoritative?
4. What should happen when the answer requires live data?

## Lab 2 — Slides 21–27

Mission: locate and explain multi-vendor config evidence without pretending RAG is a parser.

Use Demo Runbook Steps 6.1–6.7.

Key teaching moments:
- Vendor syntax differs; shared metadata provides a common retrieval layer.
- Read the source directly before asking the model so you have an answer key.
- Device filters prevent unrelated configs from contaminating the answer.
- RAG is useful for explanation and orientation; fleet-wide exactness belongs to parsers, NetBox, pyATS, Batfish, NAPALM, or vendor APIs.
- Protect the VLAN 130 mismatch exercise—it is the strongest config-correlation moment.

Backbone phrase: **RAG finds what is relevant. Deterministic tools establish exact state.**

## Lab 3 — Slides 28–34

Mission: investigate the BGP flaps without confusing timing with causality.

Use Demo Runbook Steps 7.1–7.5.

Evidence roles:
- Runbook = approved process
- Config snapshot = point-in-time observation
- Change = approved intent
- Incident = event record
- Postmortem = final historical causal conclusion

Have students build the timeline before generation:
1. CHG-1234 changed the Atlanta import prefix list.
2. Post-change validation showed Established.
3. BGP resets occurred the next day.
4. Juniper logs showed policy evaluation errors.
5. The postmortem attributes the incident to unapproved drift on New York.

Say: **“Temporal proximity is not causality.”**

Then use the firewall drift case to compare approved intent with observed config text. Remind the class that a production compliance decision still needs normalized deterministic parsing.

## Lab 4 — Slides 35–39

Mission: intentionally retrieve stale, rejected, and malicious content.

Use Demo Runbook Steps 8.1–8.5.

Key teaching moments:
- The retired BGP runbook may match the user’s language extremely well and still be unsafe.
- Retrieved prompt injection is an ingestion/retrieval problem as well as a prompting problem.
- Safe assistance refuses unauthorized action while remaining useful.
- Evals should test expected sources, factual consistency, citations, authority, conflict handling, insufficient information, safety, and reproducibility.

Ask after trap prompts:
1. Did it refuse the unauthorized part?
2. Did it remain helpful?
3. Did it identify missing approval/evidence?
4. Did it avoid claiming action was performed?

## Slides 40–41 — Application and providers

### Slide 40 — Streamlit
Show that the UI exposes the same RAG pipeline. Source visibility is a feature, not clutter.

### Slide 41 — Provider switching
Use the live switch only if credentials and time permit. Emphasize that changing the model is not the first response to bad retrieval.

## Slides 42–44 — Close

### Slide 42 — What production adds
Identity, access control, source ownership, freshness/lifecycle, hybrid retrieval, deterministic live tools, approval systems, observability, and evaluation.

### Slide 43 — Operating model
1. Knowledge
2. Retrieval
3. Validation
4. Control

Say: “Keeping these layers separate makes the system safer and easier to reason about.”

### Slide 44 — Final takeaway
> **RAG is the knowledge layer. It is not the live source of truth, deterministic validator, authorization system, or production executor.**

Close with: “The goal is not to replace network judgment. The goal is to reduce the time it takes an engineer to find the right evidence, understand the context, and choose the next safe validation step.”

Final audience question: “What NetOps knowledge source in your environment would be useful to retrieve—and what control would you require before trusting the assistant?”

## Optional Hermes Desktop bonus

Use:
- `bonus/hermes-netops-copilot/DESKTOP_PRESENTER_NOTES.md`
- `bonus/hermes-netops-copilot/BONUS_DEMO_RUNBOOK.md`

The bonus story is:

**RAG provides trusted knowledge → MCP provides controlled read-only evidence → the reusable skill provides investigation discipline → the engineer keeps production control.**

## Pacing protection

If ahead: use scenario cards, Top-K experiments, provider comparison, or extra eval design.

If behind: protect the opening generic-model demo, Lab 1 metadata filtering, Lab 2 VLAN mismatch, Lab 3 BGP causal investigation, Lab 4 source-authority/prompt-injection discussion, and the final operating-boundary slide. Skip the optional DNS case, extra unsafe prompts, and live provider switching.

If generation fails, continue with retrieval-only demonstrations from Demo Runbook Section 11. The workshop can still teach the evidence layer, metadata, source authority, stale content, and prompt injection.
