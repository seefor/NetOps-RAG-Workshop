---
change_id: CHG-1241
title: Raise OSPF Cost Toward Atlanta Distribution
service: ospf
site: atlanta-dc
device_name: atl-core-r2
status: completed
approval: approved
source_authority: approved_change
implemented_at: 2026-07-27T22:30:00-04:00
---
# CHG-1241

Changed the OSPF cost on `atl-core-r2` GigabitEthernet0/2 from 10 to 50 to prefer the alternate path during normal operation. Pre-checks and post-checks included adjacency state, routing table, path preference, latency, and application reachability.
