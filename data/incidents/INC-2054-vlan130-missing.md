---
incident_id: INC-2054
title: Server VLAN Missing on Access Uplink
service: switching
site: atlanta-dc
status: open
source_authority: incident_record
opened_at: 2026-07-31T08:55:00-04:00
---
# INC-2054

A newly connected server on VLAN 130 cannot reach its gateway. `atl-access-sw1` allows VLAN 130 on its uplink, but `atl-dist-sw1` allows only VLANs 110 and 120 on the corresponding downlink. No approved change record for the trunk mismatch has been found. Read-only validation is in progress.
