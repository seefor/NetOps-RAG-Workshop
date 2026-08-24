from __future__ import annotations

from typing import Any

from mcp.server import MCPServer

from network_state_tools import STORE

mcp = MCPServer("Synthetic Network State")


@mcp.tool()
def get_scenario_context() -> dict[str, Any]:
    """Return the active synthetic incident scenario and the devices in scope."""
    return STORE.scenario_context()


@mcp.tool()
def list_devices(site: str | None = None, service: str | None = None) -> dict[str, Any]:
    """List devices present in the active synthetic scenario."""
    return STORE.list_devices(site=site, service=service)


@mcp.tool()
def get_device_facts(device_name: str) -> dict[str, Any]:
    """Return read-only synthetic device facts."""
    return STORE.device_facts(device_name)


@mcp.tool()
def get_bgp_summary(device_name: str) -> dict[str, Any]:
    """Return synthetic current BGP state for a device."""
    return STORE.protocol_summary(device_name, "bgp")


@mcp.tool()
def get_ipsec_summary(device_name: str) -> dict[str, Any]:
    """Return synthetic current IPsec/IKE state for a device."""
    return STORE.protocol_summary(device_name, "ipsec")


@mcp.tool()
def get_interface_status(device_name: str, interface: str | None = None) -> dict[str, Any]:
    """Return synthetic current interface state."""
    return STORE.interfaces(device_name, interface=interface)


@mcp.tool()
def get_route(device_name: str, destination: str) -> dict[str, Any]:
    """Return synthetic routing-table evidence for a destination."""
    return STORE.route(device_name, destination)


@mcp.tool()
def get_recent_logs(device_name: str, contains: str | None = None, limit: int = 20) -> dict[str, Any]:
    """Return recent synthetic log events. The tool is read-only."""
    return STORE.logs(device_name, contains=contains, limit=limit)


@mcp.tool()
def get_config_diff(device_name: str) -> dict[str, Any]:
    """Return deterministic synthetic config drift relative to the approved snapshot."""
    return STORE.config_diff(device_name)


if __name__ == "__main__":
    mcp.run(transport="stdio")
