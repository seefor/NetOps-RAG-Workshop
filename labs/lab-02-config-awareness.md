# Lab 2 — Multi-Vendor Config Awareness and Metadata Filtering

**Duration:** 40 minutes

## Goal

Use RAG to find and explain relevant configuration while learning where deterministic parsing is still required.

## 1. Config scavenger hunt — 12 minutes

Use retrieval or the UI to find:

1. The interface with OSPF cost 50.
2. The VLAN 130 trunk mismatch.
3. The firewall rule with disabled logging.
4. The lab-only Arista device.
5. The decommissioned router using AS 64512.
6. The F5 load-balancing method.

Suggested command:

```bash
netops-rag retrieve "Which interface has OSPF cost 50?" --doc-type config --top-k 5
```

## 2. Device-specific filters — 8 minutes

```bash
netops-rag ask "What BGP neighbor and import policy are configured?" --device nyc-edge-r1
netops-rag ask "Which VLANs are allowed on the uplink?" --device atl-access-sw1
```

Compare filtered and unfiltered answers.

## 3. Cross-config comparison — 10 minutes

```bash
netops-rag ask "Compare the uplinks between atl-access-sw1 and atl-dist-sw1. Is VLAN 130 consistently allowed?"
```

The answer should cite both configs and avoid claiming that a change was executed.

## 4. Exactness boundary — 5 minutes

Ask:

```text
List every NTP server on every active production device and prove the list is complete.
```

Discuss why RAG may miss chunks and why exact fleet-wide inventory belongs in pyATS, NAPALM, Batfish, a CMDB, NetBox, or a parser.

## 5. Debrief — 5 minutes

> Runbooks tell us what should happen. Configs provide evidence of what appears to be configured. Neither replaces live state or deterministic validation.

## Stretch challenge

Filter to `--site atlanta-dc --doc-type config` and ask a question that should not return the New York or lab devices.
