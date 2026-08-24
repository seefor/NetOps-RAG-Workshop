# Lab 1 — Build and Inspect the NetOps Knowledge Base

**Duration:** 40 minutes  
**Pattern:** Explain → build → inspect → break → improve → debrief

## Goal

Index the AtlasNet dataset, understand chunks and metadata, and prove that retrieval quality must be inspected before answer quality.

## 1. Inspect the dataset — 5 minutes

```bash
netops-rag stats --data data
netops-rag catalog --data data --doc-type runbook
```

Discuss the mix of approved, retired, lab-only, and untrusted sources.

## 2. Ingest — 5 minutes

```bash
cp .env.example .env
netops-rag ingest --data data --reset
```

Record the document and chunk counts.

## 3. Compare broad and specific retrieval — 10 minutes

```bash
netops-rag retrieve "BGP is down. What should I check?" --top-k 5
netops-rag retrieve "The BGP session between atl-core-r1 and nyc-edge-r1 is flapping after a policy edit. What should I validate first?" --top-k 5
```

Identify which entities improved retrieval: protocol, devices, symptom, and change context.

## 4. Top-K experiment — 8 minutes

Run the same question with `--top-k 2`, `--top-k 5`, and `--top-k 10`. Discuss missing evidence versus noisy context.

## 5. Stale-source challenge — 7 minutes

```bash
netops-rag retrieve "What should I do first when BGP is down?" --top-k 8
netops-rag retrieve "What should I do first when BGP is down?" --top-k 8 --status active
```

Find the retired 2024 note and explain why similarity alone does not establish authority.

## 6. Debrief — 5 minutes

- Which source ranked first?
- Did a retired source appear?
- What metadata would you require in a production knowledge base?
- Why should engineers inspect retrieval before trusting generation?

## Instructor talk track

> We are not teaching the model our network. We are building a searchable evidence layer and deciding which evidence is allowed to influence an answer.

Emphasize that embeddings find semantic similarity, while metadata and source governance determine operational relevance.

## Stretch challenge

Change `CHUNK_SIZE` in `.env`, reset the collection, and compare how the same config or runbook is split and retrieved.
