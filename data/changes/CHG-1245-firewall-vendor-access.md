---
change_id: CHG-1245
title: Temporary Vendor Support Access
service: firewall
site: atlanta-dc
device_name: fw-edge-01
status: implemented_with_exception
approval: approved
source_authority: approved_change
implemented_at: 2026-07-30T19:00:00-04:00
expires_at: 2026-08-02T19:00:00-04:00
---
# CHG-1245

Created `vendor-support-temp` for source `198.51.100.77` to destination `10.10.130.45`. The approved request specified TCP 443 only, logging at session end, and automatic expiration on August 2. The observed config currently shows `application any`, `service any`, and logging disabled, so the implementation does not match the approved scope and requires review.
