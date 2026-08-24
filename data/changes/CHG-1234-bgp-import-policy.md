---
change_id: CHG-1234
title: Update Atlanta BGP Import Prefix List
service: bgp
site: atlanta-dc
device_name: atl-core-r1
status: completed
approval: approved
source_authority: approved_change
implemented_at: 2026-07-29T22:15:00-04:00
---
# CHG-1234

Updated `PL-NYC-IN` on `atl-core-r1` to allow `10.20.0.0/16 le 24`. Validation showed the BGP session remained Established and approved NYC prefixes were received. Rollback was to restore the previous prefix-list. No rollback was required.
