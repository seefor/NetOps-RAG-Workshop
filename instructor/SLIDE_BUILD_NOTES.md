# Slide Build Notes — Sif Baksh Style

Use this as the creative direction when building the deck.

## Visual style

- Dark navy / blueprint background
- Cyan highlights for AI, retrieval, and context paths
- Amber highlights for warnings, guardrails, and safety boundaries
- Use network diagrams, config snippets, terminal screenshots, and simple architecture flows
- Keep slides practical and technical, not academic

## Recommended slide sections

1. **Problem framing**
   - Knowledge is scattered
   - Generic AI is risky
   - NetOps needs grounded answers

2. **Architecture**
   - RAG loop
   - NetOps data sources
   - Provider-flexible stack

3. **Lab 1**
   - Runbook ingestion
   - Retrieval debugging
   - Answer with sources

4. **Lab 2**
   - Config awareness
   - RAG for explanation
   - Deterministic tools for validation

5. **Lab 3**
   - Multi-source troubleshooting
   - Better questions retrieve better context
   - Operational answer pattern

6. **Lab 4**
   - Guardrails
   - Unsafe prompt tests
   - Evaluation

7. **Capstone and close**
   - Pick one workflow
   - Start with trusted sources
   - RAG is the knowledge layer

## Design patterns to use

### Pattern 1 — Split-screen comparison

Use for:

- Generic AI vs grounded AI
- RAG vs deterministic parser
- Safe troubleshooting vs unsafe change execution

### Pattern 2 — Pipeline diagram

Use for:

- Ingestion
- Retrieval
- Provider switching
- Eval loop

### Pattern 3 — Operational checklist

Use for:

- What good looks like
- Guardrails
- Capstone success criteria

### Pattern 4 — Terminal-first demo slide

Use for:

- Commands students will run
- Retrieval output
- Ask output
- Eval output

## Suggested visual metaphors

- RAG as the “context layer” between the engineer and the model
- Vector database as a searchable operational memory
- Guardrails as a change-control boundary
- Evals as regression tests for AI behavior
- Config parsers as instruments, RAG as the copilot that explains where to look

## Tone guidance

Keep the language practical:

Instead of:

> “This lab demonstrates semantic retrieval over vectorized operational corpora.”

Say:

> “This lab shows how the assistant finds the right runbook before it answers.”

Instead of:

> “We use embeddings to project text into latent space.”

Say:

> “Embeddings let us search by meaning, not just exact keywords.”

Instead of:

> “The system has policy-aligned refusal behavior.”

Say:

> “The assistant should know when it does not have enough approved context to recommend a production change.”
