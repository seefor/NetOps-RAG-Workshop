# Presenter Notes — Hermes Desktop NetOps Bonus

Use `DESKTOP_PRESENTER_NOTES.md` as the detailed version. These notes are the short presenter card.

## The story

**RAG gave us knowledge. Hermes Desktop makes the next layer visible.**

Show:

```text
RAG knowledge + read-only operational evidence + reusable skill
                              ↓
                       Incident Copilot
```

## What to emphasize

- The Desktop app is only the interface; the same Hermes Agent core is underneath.
- The bonus uses a dedicated `netops-workshop` profile.
- The two MCP servers are intentionally read-only.
- RAG answers "what do our trusted sources say?"
- State tools answer "what are we observing now?"
- The skill defines *how* an investigation should proceed.
- The engineer still authorizes production action.

## Visual wow moments

1. Show the MCP servers and limited tool surface in Settings.
2. Run RAG-only and ask the room what current evidence is missing.
3. Paste the full incident prompt and leave streaming tool activity visible.
4. Switch the scenario from the integrated terminal.
5. Show the same skill handling an IPsec incident.
6. Open the Skills pane and show that the investigation process is reusable.

## Closing line

> The interesting part is not that AI can talk about BGP. It is that it can gather the right evidence, show where it came from, follow a repeatable process, and still remain outside the production change boundary.
