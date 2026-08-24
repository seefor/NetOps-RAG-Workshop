---
title: Firewall Rule Review
service: firewall
status: active
approval: approved
source_authority: security_runbook
owner: Network Security
last_reviewed: 2026-07-16
---
# Firewall Rule Review

Review source, destination, application, service, action, logging, owner, business justification, expiration, and zone direction. Flag broad `any` use, disabled logging, temporary rules without expiration, shadowed rules, and rules that bypass application-default behavior. A rule may be high risk even when source IP is restricted if destination, application, and service are all broad.
