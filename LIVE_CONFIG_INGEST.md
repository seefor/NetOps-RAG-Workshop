# Live Multi-Vendor Config Collection and Ingestion

This optional workflow extends the workshop from static synthetic snapshots to read-only SSH collection from real network devices.

The important design choice is that the collector **does not write directly to ChromaDB with its own embedding logic**. It saves the retrieved running configuration as a normal workshop source file with YAML frontmatter and then reuses the existing `netops_rag.ingest` pipeline. That keeps chunking, embeddings, metadata, and the Chroma collection consistent with the rest of the workshop.

## 1. Install the optional live-network dependency

From the workshop virtual environment:

```bash
python -m pip install -e ".[live-network]"
```

This adds Netmiko while keeping the normal workshop dependency set unchanged.

## 2. Create your device inventory

Copy the example:

```bash
cp inventory.example.yaml inventory.yaml
```

Edit `inventory.yaml` with your own management addresses, device types, sites, roles, and services.

Do not place usernames or passwords in the YAML file. `inventory.yaml` is excluded by `.gitignore`.

Supported example Netmiko device types:

```text
cisco_ios
arista_eos
juniper_junos
paloalto_panos
f5_tmsh
```

Each device may override the default read-only collection command with a `command:` value if required.

## 3. Provide SSH credentials

The default credential profile is `NETOPS`.

macOS/Linux:

```bash
export NETOPS_USERNAME="your-username"
export NETOPS_PASSWORD="your-password"
```

If privileged mode is required on a Cisco-style device:

```bash
export NETOPS_SECRET="your-enable-secret"
```

If the variables are not present, the collector prompts once before starting worker threads.

## 4. Collect configs only

```bash
python scripts/collect_device_configs.py \
  --inventory inventory.yaml
```

The latest source for each device is written under:

```text
data/configs/live/current/
```

Timestamped history copies are written under:

```text
data/configs/live/history/
```

The live directory is excluded from Git because real running configurations may contain credentials, shared secrets, SNMP strings, keys, internal addressing, or other sensitive information.

## 5. Collect and ingest into the existing ChromaDB

Use:

```bash
python scripts/collect_device_configs.py \
  --inventory inventory.yaml \
  --ingest
```

The workflow is:

```text
SSH device
   ↓
running config
   ↓
workshop YAML frontmatter
   ↓
data/configs/live/current/<device>.cfg|.conf
   ↓
existing netops_rag.ingest pipeline
   ↓
existing chunk_text()
   ↓
configured embedding provider
   ↓
existing Chroma collection
```

Before re-ingesting a device's fixed `current` source file, the collector removes the old Chroma chunks for that source path. This prevents stale chunks from an earlier running config from remaining searchable after the file changes.

The retained metadata follows the same workshop pattern and adds collection-time fields:

```text
device_name
site
role
vendor
platform
service
status
environment
source_authority=device_snapshot
snapshot_date
snapshot_timestamp
collection_method=ssh
collection_command
management_address
doc_type=config
```

The normal ingestion pipeline then adds its standard source, filename, directory, chunk index, and chunk count metadata.

## 6. Verify retrieval

For one device:

```bash
netops-rag retrieve \
  "What BGP policy is configured?" \
  --device atl-core-r1 \
  --doc-type config
```

For two devices:

```bash
netops-rag ask \
  "Compare the BGP configuration on atl-core-r1 and nyc-edge-r1" \
  --device atl-core-r1 \
  --device nyc-edge-r1 \
  --doc-type config
```

## 7. Important operational boundary

A configuration retrieved over SSH is strong point-in-time evidence, but after it is stored in Chroma it is still a **device snapshot**, not a live-state query.

Keep:

```text
source_authority=device_snapshot
```

Do not relabel indexed configuration as `live_state`.

Use a separate read-only operational-state tool or MCP integration when you need current BGP state, interface state, routes, logs, counters, or other telemetry.
