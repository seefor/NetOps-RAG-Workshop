#!/usr/bin/env python3
"""Collect read-only multi-vendor running configs and ingest them into workshop ChromaDB.

The collector writes each device's latest configuration as a normal workshop source file
with YAML frontmatter, then reuses the existing NetOps RAG ingestion pipeline. It does not
implement a second chunking, embedding, or vector-store path.

Supported Netmiko device types in the example inventory:
- cisco_ios
- arista_eos
- juniper_junos
- paloalto_panos
- f5_tmsh

Credentials are read from environment variables (or prompted once per credential profile)
and are never written to the inventory or snapshot files.
"""

from __future__ import annotations

import argparse
import getpass
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from netmiko import ConnectHandler

from netops_rag.config import get_settings
from netops_rag.ingest import ingest
from netops_rag.vectorstore import get_collection


PLATFORMS: dict[str, dict[str, str]] = {
    "cisco_ios": {
        "vendor": "cisco",
        "platform": "ios-xe",
        "command": "show running-config",
        "extension": ".cfg",
    },
    "arista_eos": {
        "vendor": "arista",
        "platform": "eos",
        "command": "show running-config",
        "extension": ".cfg",
    },
    "juniper_junos": {
        "vendor": "juniper",
        "platform": "junos",
        "command": "show configuration | display set | no-more",
        "extension": ".conf",
    },
    "paloalto_panos": {
        "vendor": "paloalto",
        "platform": "pan-os",
        "command": "show config running",
        "extension": ".conf",
    },
    "f5_tmsh": {
        "vendor": "f5",
        "platform": "tmos",
        "command": "list /",
        "extension": ".conf",
    },
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def load_inventory(path: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    devices = data.get("devices", [])
    if not isinstance(devices, list):
        raise ValueError("inventory must contain a 'devices:' list")
    return devices


def credential_profiles(devices: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    """Resolve credentials once per profile before worker threads start."""
    resolved: dict[str, dict[str, str]] = {}
    profiles = sorted({str(d.get("credential_profile", "NETOPS")).upper() for d in devices})

    for profile in profiles:
        username = os.getenv(f"{profile}_USERNAME", "").strip()
        password = os.getenv(f"{profile}_PASSWORD", "")
        secret = os.getenv(f"{profile}_SECRET", "")

        if not username:
            username = input(f"{profile} SSH username: ").strip()
        if not password:
            password = getpass.getpass(f"{profile} SSH password: ")

        resolved[profile] = {
            "username": username,
            "password": password,
            "secret": secret,
        }

    return resolved


def collect_config(
    device: dict[str, Any],
    credentials: dict[str, dict[str, str]],
) -> tuple[str, dict[str, Any], str]:
    name = str(device["name"])
    host = str(device["host"])
    device_type = str(device["device_type"])

    if device_type not in PLATFORMS:
        raise ValueError(
            f"{name}: unsupported device_type '{device_type}'. "
            f"Supported: {', '.join(sorted(PLATFORMS))}"
        )

    platform = PLATFORMS[device_type]
    profile = str(device.get("credential_profile", "NETOPS")).upper()
    auth = credentials[profile]
    command = str(device.get("command", platform["command"]))

    connection_args: dict[str, Any] = {
        "device_type": device_type,
        "host": host,
        "username": auth["username"],
        "password": auth["password"],
        "port": int(device.get("port", 22)),
        "conn_timeout": int(device.get("connect_timeout", 15)),
        "banner_timeout": int(device.get("banner_timeout", 30)),
        "auth_timeout": int(device.get("auth_timeout", 30)),
        "fast_cli": False,
    }

    if auth.get("secret"):
        connection_args["secret"] = auth["secret"]

    key_file = device.get("key_file")
    if key_file:
        connection_args["use_keys"] = True
        connection_args["key_file"] = os.path.expanduser(str(key_file))

    print(f"[CONNECT] {name} ({host})")
    connection = ConnectHandler(**connection_args)

    try:
        if bool(device.get("enable", False)):
            connection.enable()
        config = connection.send_command(
            command,
            read_timeout=int(device.get("read_timeout", 120)),
            strip_prompt=True,
            strip_command=True,
        )
    finally:
        connection.disconnect()

    config = config.strip()
    if not config:
        raise RuntimeError(f"{name}: device returned an empty configuration")

    now = utc_now()
    metadata: dict[str, Any] = {
        "device_name": name,
        "site": device.get("site", "unknown"),
        "role": device.get("role", "unknown"),
        "vendor": device.get("vendor", platform["vendor"]),
        "platform": device.get("platform", platform["platform"]),
        "service": device.get("service", "network"),
        "status": "active",
        "environment": device.get("environment", "production"),
        "source_authority": "device_snapshot",
        "snapshot_date": now.strftime("%Y-%m-%d"),
        "snapshot_timestamp": now.isoformat(),
        "collection_method": "ssh",
        "collection_command": command,
        "management_address": host,
        "doc_type": "config",
    }
    return config, metadata, platform["extension"]


def write_snapshot(
    device_name: str,
    config: str,
    metadata: dict[str, Any],
    extension: str,
    current_dir: Path,
    history_dir: Path | None,
) -> Path:
    """Write one fixed current source per device plus an optional history copy."""
    device_current_dir = current_dir / device_name
    device_current_dir.mkdir(parents=True, exist_ok=True)
    current_path = device_current_dir / f"{device_name}{extension}"

    frontmatter = yaml.safe_dump(metadata, sort_keys=False, default_flow_style=False).strip()
    content = f"---\n{frontmatter}\n---\n{config}\n"
    current_path.write_text(content, encoding="utf-8")

    if history_dir is not None:
        stamp = str(metadata["snapshot_timestamp"]).replace(":", "").replace("+0000", "Z")
        device_history = history_dir / device_name
        device_history.mkdir(parents=True, exist_ok=True)
        (device_history / f"{device_name}-{stamp}{extension}").write_text(content, encoding="utf-8")

    return current_path


def remove_previous_chunks(source_path: Path) -> None:
    """Remove previous Chroma chunks for a fixed current-source path before re-ingestion."""
    collection = get_collection(get_settings())
    collection.delete(where={"source": source_path.as_posix()})


def ingest_current_snapshot(source_path: Path) -> int:
    """Reuse the workshop ingestion pipeline for exactly one successful device."""
    remove_previous_chunks(source_path)
    return ingest(source_path.parent, get_settings(), reset=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect read-only running configs and optionally ingest them into NetOps RAG"
    )
    parser.add_argument("--inventory", default="inventory.yaml")
    parser.add_argument("--current-dir", default="data/configs/live/current")
    parser.add_argument("--history-dir", default="data/configs/live/history")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="After collection, ingest each successful current snapshot with the workshop pipeline",
    )
    parser.add_argument(
        "--no-history",
        action="store_true",
        help="Do not retain timestamped history copies on disk",
    )
    args = parser.parse_args()

    inventory_path = Path(args.inventory)
    current_dir = Path(args.current_dir)
    history_dir = None if args.no_history else Path(args.history_dir)

    devices = load_inventory(inventory_path)
    if not devices:
        raise SystemExit("No devices found in inventory")

    credentials = credential_profiles(devices)
    successes: list[Path] = []
    failures = 0

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(collect_config, device, credentials): device
            for device in devices
        }
        for future in as_completed(futures):
            device = futures[future]
            name = str(device.get("name", "unknown"))
            try:
                config, metadata, extension = future.result()
                path = write_snapshot(
                    name,
                    config,
                    metadata,
                    extension,
                    current_dir,
                    history_dir,
                )
                successes.append(path)
                print(f"[OK] {name} -> {path}")
            except Exception as exc:
                failures += 1
                print(f"[FAIL] {name}: {exc}")

    total_chunks = 0
    ingest_failures = 0
    if args.ingest:
        for source_path in successes:
            try:
                print(f"[INGEST] {source_path}")
                count = ingest_current_snapshot(source_path)
                total_chunks += count
                print(f"[INGEST OK] {source_path.name}: {count} chunks")
            except Exception as exc:
                ingest_failures += 1
                print(f"[INGEST FAIL] {source_path}: {exc}")

    print("\nCollection summary")
    print(f"  successful devices: {len(successes)}")
    print(f"  collection failures:{failures:>3}")
    print(f"  current snapshots:  {current_dir}")
    if history_dir is not None:
        print(f"  history snapshots:  {history_dir}")
    print(f"  Chroma updated:      {'yes' if args.ingest and successes else 'no'}")
    if args.ingest:
        print(f"  indexed chunks:      {total_chunks}")
        print(f"  ingestion failures:  {ingest_failures}")

    if failures or ingest_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
