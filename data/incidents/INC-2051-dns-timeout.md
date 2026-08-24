---
incident_id: INC-2051
title: Atlanta Clients Experienced DNS Timeouts
service: dns
site: atlanta-dc
status: resolved
source_authority: incident_record
opened_at: 2026-07-31T07:40:00-04:00
resolved_at: 2026-07-31T08:22:00-04:00
---
# INC-2051

Clients in VLAN 110 experienced intermittent DNS timeouts. DHCP options were correct. Resolver `192.0.2.53` showed high latency while `192.0.2.54` was healthy. Traffic was temporarily shifted to the healthy resolver under emergency change. Planned change `CHG-1250` is still scheduled and was not the cause because it had not been implemented.
