---
incident_id: INC-2048
title: Atlanta to New York BGP Session Flapping
service: bgp
site: atlanta-dc
status: resolved
source_authority: incident_record
opened_at: 2026-07-30T09:12:00-04:00
resolved_at: 2026-07-30T10:04:00-04:00
---
# INC-2048

Symptoms: the eBGP session between `atl-core-r1` and `nyc-edge-r1` reset three times. Underlay reachability remained stable. Logs on the Juniper peer reported import-policy evaluation errors after an unapproved manual edit to `IMPORT-ATL`. The policy was restored through approved emergency change `ECHG-77`. The session stabilized and route counts returned to baseline.
