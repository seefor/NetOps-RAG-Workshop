# Lab 3 — Multi-Source NetOps Incident Investigation

**Duration:** 40 minutes

## Goal

Correlate runbooks, configs, changes, incidents, postmortems, and policy into a grounded troubleshooting answer.

## 1. Initial incident prompt — 5 minutes

```bash
netops-rag ask "The BGP session between atl-core-r1 and nyc-edge-r1 flapped this morning. Was CHG-1234 the cause?"
```

## 2. Inspect retrieval — 8 minutes

```bash
netops-rag retrieve "The BGP session between atl-core-r1 and nyc-edge-r1 flapped this morning. Was CHG-1234 the cause?" --top-k 10
```

Look for the runbook, two configs, change, incident, postmortem, and any distracting retired or untrusted source.

## 3. Improve the question — 7 minutes

Ask for evidence, uncertainty, and a safe next step:

```bash
netops-rag ask "Using current approved sources, determine whether CHG-1234 caused the atl-core-r1 to nyc-edge-r1 BGP flaps. Separate facts from hypotheses, cite evidence, and list read-only validation before any change."
```

## 4. Group scenario — 12 minutes

Choose one scenario from `scenarios/SCENARIO_CARDS.md`:

- VLAN 130 mismatch
- Firewall implementation drift
- DNS timeout timeline
- IPsec VPN investigation
- Load balancer pool failure

Each group must report:

1. The best source.
2. One conflicting or irrelevant source.
3. What is known.
4. What remains unknown.
5. What should be validated next.
6. What should not be changed yet.

## 5. Debrief — 8 minutes

Discuss how a real incident requires multiple evidence types. A good answer should identify causal evidence, not merely retrieve documents containing the same protocol name.

## Instructor talk track

> This is where RAG becomes operationally useful: not because it knows BGP, but because it can bring the runbook, current configs, incident timeline, and approved change into the same answer.
