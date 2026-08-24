---
title: DNS Resolution Failure
service: dns
status: active
approval: approved
source_authority: operations_runbook
owner: Core Services
last_reviewed: 2026-07-14
---
# DNS Resolution Failure

Determine whether failure is client-specific, site-specific, record-specific, or global. Compare queries to the local resolver and a known healthy resolver. Check DHCP-provided DNS servers, resolver health, forwarding, response codes, latency, and recent record changes. Separate authoritative DNS failures from recursive resolver failures. Capture the exact query name, type, server, and timestamp.
