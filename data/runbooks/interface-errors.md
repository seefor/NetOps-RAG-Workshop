---
title: Interface Errors and Packet Loss
service: interfaces
status: active
approval: approved
source_authority: operations_runbook
owner: Network Operations
last_reviewed: 2026-07-12
---
# Interface Errors and Packet Loss

Collect interface counters twice, separated by at least 60 seconds. Determine whether CRC, input errors, output drops, overruns, or carrier transitions are increasing. Validate speed, duplex, optic type, signal levels, cable or fiber path, and the far-end interface. A single historical counter value is not proof of an active fault. Preserve timestamps and both-end evidence before replacing hardware.
