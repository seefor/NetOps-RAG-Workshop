from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class ScenarioStore:
    def __init__(self, base_dir: Path | None = None, scenario_override: str | None = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parents[1] / "mock_state"
        self.scenario_override = scenario_override
        self.active_file = self.base_dir / ".active_scenario"

    def list_scenarios(self) -> list[str]:
        return sorted(
            path.name
            for path in self.base_dir.iterdir()
            if path.is_dir() and (path / "scenario.json").exists()
        )

    def active_scenario_id(self) -> str:
        if self.scenario_override:
            return self.scenario_override
        env_value = os.getenv("NETOPS_MOCK_SCENARIO")
        if env_value:
            return env_value
        if self.active_file.exists():
            return self.active_file.read_text(encoding="utf-8").strip()
        return "bgp-policy-drift"

    def load_scenario(self) -> dict[str, Any]:
        scenario_id = self.active_scenario_id()
        path = self.base_dir / scenario_id / "scenario.json"
        if not path.exists():
            raise ValueError(f"Unknown scenario '{scenario_id}'. Valid: {', '.join(self.list_scenarios())}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _device(self, device_name: str) -> tuple[dict[str, Any], dict[str, Any]]:
        scenario = self.load_scenario()
        device = scenario.get("devices", {}).get(device_name)
        if device is None:
            return scenario, {
                "error": "device_not_in_scenario",
                "device_name": device_name,
                "available_devices": sorted(scenario.get("devices", {})),
            }
        return scenario, device

    def scenario_context(self) -> dict[str, Any]:
        scenario = self.load_scenario()
        return {
            key: value
            for key, value in scenario.items()
            if key not in {"devices"}
        } | {"devices": sorted(scenario.get("devices", {}))}

    def list_devices(self, site: str | None = None, service: str | None = None) -> dict[str, Any]:
        scenario = self.load_scenario()
        devices = []
        for name, data in scenario.get("devices", {}).items():
            facts = data.get("facts", {})
            if site and facts.get("site") != site:
                continue
            if service and service not in data.get("services", []):
                continue
            devices.append({"device_name": name, "facts": facts, "services": data.get("services", [])})
        return {"scenario": scenario["id"], "count": len(devices), "devices": devices}

    def device_facts(self, device_name: str) -> dict[str, Any]:
        scenario, device = self._device(device_name)
        if "error" in device:
            return device
        return self._envelope(scenario, device_name, "facts", device.get("facts", {}))

    def protocol_summary(self, device_name: str, protocol: str) -> dict[str, Any]:
        scenario, device = self._device(device_name)
        if "error" in device:
            return device
        data = device.get(protocol)
        if data is None:
            return {
                "scenario": scenario["id"],
                "device_name": device_name,
                "protocol": protocol,
                "available": False,
                "message": f"No {protocol} state exists for this device in the active scenario.",
            }
        return self._envelope(scenario, device_name, protocol, data)

    def interfaces(self, device_name: str, interface: str | None = None) -> dict[str, Any]:
        scenario, device = self._device(device_name)
        if "error" in device:
            return device
        items = device.get("interfaces", [])
        if interface:
            items = [item for item in items if item.get("name") == interface]
        return self._envelope(scenario, device_name, "interfaces", items)

    def route(self, device_name: str, destination: str) -> dict[str, Any]:
        scenario, device = self._device(device_name)
        if "error" in device:
            return device
        routes = device.get("routes", [])
        wanted = destination.split("/", 1)[0]
        matches = [
            route for route in routes
            if route.get("destination") == destination
            or str(route.get("destination", "")).split("/", 1)[0] == wanted
        ]
        return self._envelope(scenario, device_name, "routes", matches)

    def logs(self, device_name: str, contains: str | None = None, limit: int = 20) -> dict[str, Any]:
        scenario, device = self._device(device_name)
        if "error" in device:
            return device
        logs = device.get("logs", [])
        if contains:
            needle = contains.lower()
            logs = [entry for entry in logs if needle in json.dumps(entry).lower()]
        logs = logs[-max(1, min(limit, 100)):]
        return self._envelope(scenario, device_name, "logs", logs)

    def config_diff(self, device_name: str) -> dict[str, Any]:
        scenario, device = self._device(device_name)
        if "error" in device:
            return device
        return self._envelope(scenario, device_name, "config_diff", device.get("config_diff", {}))

    @staticmethod
    def _envelope(
        scenario: dict[str, Any], device_name: str, evidence_type: str, data: Any
    ) -> dict[str, Any]:
        return {
            "scenario": scenario["id"],
            "observed_at": scenario["observed_at"],
            "synthetic": True,
            "read_only": True,
            "device_name": device_name,
            "evidence_type": evidence_type,
            "data": data,
        }


STORE = ScenarioStore()
