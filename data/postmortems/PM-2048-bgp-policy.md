---
postmortem_id: PM-2048
title: BGP Policy Drift Caused Session Resets
service: bgp
site: new-york-dc
status: final
source_authority: postmortem
published_at: 2026-07-31
---
# PM-2048

The incident was caused by policy drift on `nyc-edge-r1`, not by `CHG-1234` on `atl-core-r1`. A manual edit introduced an invalid policy term. Corrective actions: require configuration backup before edge policy changes, add deterministic syntax validation, and alert on configuration drift. RAG can correlate the runbook, configs, and incident timeline, but exact drift detection must use configuration comparison tooling.
