---
title: BGP Neighbor Down
service: bgp
status: active
approval: approved
source_authority: operations_runbook
owner: Network Engineering
last_reviewed: 2026-07-15
---
# BGP Neighbor Down

## Scope
Use this runbook when an established eBGP or iBGP session transitions to Idle, Connect, or Active.

## Read-only checks
1. Confirm the exact local device, peer address, VRF, and timestamp.
2. Check interface state and IP reachability to the peer.
3. Compare the configured local and remote AS numbers.
4. Validate update-source or local-address configuration on both peers.
5. Review authentication settings without exposing secrets.
6. Check address-family activation and route-policy references.
7. Review logs and the most recent approved change record.

## Suggested validation commands
Use the vendor-equivalent read-only commands approved for the environment:
- `show ip bgp summary`
- `show bgp neighbor <peer>`
- `show ip route <peer>`
- `show logging | include BGP`

## Escalation
Escalate when the underlay is reachable, configuration appears aligned, and the session remains down, or when a production change is required.

## Safety
Do not clear the BGP session, remove policy, or change authentication until impact, rollback, and approval are documented.
