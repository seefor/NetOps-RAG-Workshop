---
title: Load Balancer Pool Member Down
service: application-delivery
status: active
approval: approved
source_authority: operations_runbook
owner: Application Delivery
last_reviewed: 2026-07-05
---
# Load Balancer Pool Member Down

Identify the virtual server, pool, member, monitor, and failure timestamp. Check monitor status, direct member reachability, service port, TLS behavior, application response, and recent deployment changes. Do not force a member up when the health monitor is failing without application-owner approval.
