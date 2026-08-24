# AtlasNet Synthetic Dataset Guide

The workshop uses a fictional enterprise environment named **AtlasNet**. All names, addresses, incidents, policies, configurations, and change records are synthetic.

The dataset is intentionally messy because useful RAG testing needs more than perfect documents. You will find current sources, retired sources, rejected changes, decommissioned devices, lab data, and untrusted content.

## Source categories

- `data/runbooks/` — operational troubleshooting procedures
- `data/configs/` — point-in-time configuration snapshots
- `data/policies/` — operational policies and control standards
- `data/changes/` — approved, completed, scheduled, and rejected changes
- `data/incidents/` — incident records and timelines
- `data/postmortems/` — final causal conclusions
- `data/inventory/` — synthetic source-of-truth style inventory
- `data/untrusted/` — deliberately untrusted text used for prompt-injection exercises

## Important teaching traps

1. **Retired runbooks can still be semantically similar.** Students must not equate similarity with authority.
2. **Rejected changes describe requested intent, not approved work.**
3. **Config snapshots are evidence, not guaranteed live state.**
4. **Postmortems may carry the strongest causal conclusion but are not substitutes for current telemetry.**
5. **Untrusted text may contain instructions that must be treated as data, not as commands to the model.**

## Main scenarios

### BGP policy drift

The central incident involves `atl-core-r1` and `nyc-edge-r1`. The dataset contains an approved change, incident record, device snapshots, logs, and a postmortem. Students must avoid blaming the approved change purely because it occurred near the incident.

### VLAN 130 mismatch

`atl-access-sw1` and `atl-dist-sw1` contain mismatched trunk membership for VLAN 130. This is used to teach targeted config retrieval and the boundary between RAG explanation and deterministic config validation.

### Firewall drift

The `vendor-support-temp` rule on `fw-edge-01` does not fully match approved intent. Students compare the change record with the observed snapshot and discuss what still requires normalized policy parsing.

### Branch IPsec certificate expiry

The Hermes bonus introduces a second scenario where the WAN route exists, the tunnel fails authentication, and the branch identity certificate is expired. This demonstrates skill reuse across different incident domains.
