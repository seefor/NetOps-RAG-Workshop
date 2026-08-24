# Presenter Notes — Hermes Desktop Bonus

## Slide 1 — From RAG Assistant to Incident Copilot

**Visual:** RAG knowledge on the left, Hermes Desktop in the center, read-only state tools on the right.

Say:

> Everything we built today becomes more useful when an agent can decide which evidence it needs next. I am not replacing RAG. I am putting an orchestration layer on top of it.

## Slide 2 — One Desktop, Three Layers

On screen:

```text
Hermes Desktop
  → NetOps RAG MCP
  → Network State MCP
  → NetOps Investigation Skill
```

Say:

> The desktop is the user experience. RAG is still the knowledge layer. MCP is the controlled connection to evidence. The skill is the operating procedure.

## Slide 3 — Safety Is Visible

Show the Desktop MCP/tool settings.

Say:

> I want you to notice what is missing. There is no push-config tool, no reload tool, no clear-BGP tool. We are enforcing the pilot boundary structurally, not just through a system prompt.

## Slide 4 — Intent vs. Operational State

On screen:

```text
Runbook/config/change record = intent and context
Live/read-only tools          = observed state
```

Say:

> A runbook can tell me what should be checked. It cannot tell me what BGP is doing at this second. An old config can tell me what we captured. It does not prove what is running now.

## Slide 5 — Watch the Tool Activity

During the first investigation, keep Hermes Desktop's streaming tool activity visible.

Say:

> Do not watch the answer first. Watch the evidence gathering. Which source is the agent using? Is it retrieving a document, reading current state, or doing a deterministic comparison?

## Slide 6 — Same Skill, Different Incident

Switch from BGP to IPsec.

Say:

> If I had hard-coded a BGP workflow, this would fall apart now. The skill captures an investigation pattern, so it transfers to another operational domain.

## Slide 7 — The Take-Home Path

On screen:

```text
Today: synthetic state
Next: pyATS / NetBox / NAPALM / Batfish
Later: approval-gated automation
```

Say:

> Your next step is not to give an agent enable mode. Your next step is to replace one synthetic read-only evidence source with a real read-only source and evaluate the quality of the investigation.

## Closing line

> The wow factor is not that an AI can talk about BGP. The wow factor is that it can gather the right evidence, show you where it came from, reuse a governed process, and still know that it is not authorized to touch production.
