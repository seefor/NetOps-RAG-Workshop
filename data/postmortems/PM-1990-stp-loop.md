---
postmortem_id: PM-1990
title: Unmanaged Switch Triggered Campus Loop
service: spanning-tree
site: atlanta-dc
status: final
source_authority: postmortem
published_at: 2026-05-20
---
# PM-1990

An unmanaged switch connected two access ports and created a loop. BPDU Guard was missing on one legacy port. Corrective actions included enabling BPDU Guard on all edge ports, verifying root placement, and adding a configuration compliance check.
