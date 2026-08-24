from __future__ import annotations

from typing import Any

from mcp.server import MCPServer

from knowledge_tools import SERVICE

mcp = MCPServer("NetOps RAG Knowledge")


@mcp.tool()
def search_network_knowledge(
    query: str,
    top_k: int = 5,
    device_name: str | None = None,
    site: str | None = None,
    doc_type: str | None = None,
    service: str | None = None,
    status: str | None = None,
    source_authority: str | None = None,
) -> dict[str, Any]:
    """Search indexed NetOps knowledge with optional metadata filters."""
    return SERVICE.search(
        query=query,
        top_k=top_k,
        device_name=device_name,
        site=site,
        doc_type=doc_type,
        service=service,
        status=status,
        source_authority=source_authority,
    )


@mcp.tool()
def retrieve_runbook(service: str, query: str | None = None, top_k: int = 4) -> dict[str, Any]:
    """Retrieve the active approved runbook for a network service."""
    return SERVICE.search(
        query=query or f"{service} troubleshooting runbook read-only checks escalation safety",
        top_k=top_k,
        service=service,
        doc_type="runbook",
        status="active",
    )


@mcp.tool()
def retrieve_device_config(device_name: str, query: str | None = None, top_k: int = 4) -> dict[str, Any]:
    """Retrieve indexed configuration chunks for one device snapshot."""
    return SERVICE.search(
        query=query or f"configuration for {device_name}",
        top_k=top_k,
        device_name=device_name,
        doc_type="config",
    )


@mcp.tool()
def retrieve_change_record(
    query: str,
    device_name: str | None = None,
    service: str | None = None,
    top_k: int = 4,
) -> dict[str, Any]:
    """Retrieve relevant change records; status and approval remain visible in metadata."""
    return SERVICE.search(
        query=query,
        top_k=top_k,
        device_name=device_name,
        service=service,
        doc_type="change_record",
    )


@mcp.tool()
def retrieve_incident_record(query: str, service: str | None = None, top_k: int = 4) -> dict[str, Any]:
    """Retrieve historical incident records for context, not proof of current state."""
    return SERVICE.search(query=query, top_k=top_k, service=service, doc_type="incident")


@mcp.tool()
def retrieve_postmortem(query: str, service: str | None = None, top_k: int = 4) -> dict[str, Any]:
    """Retrieve final postmortems and corrective-action context."""
    return SERVICE.search(query=query, top_k=top_k, service=service, doc_type="postmortem")


@mcp.tool()
def list_sources(
    doc_type: str | None = None,
    service: str | None = None,
    status: str | None = None,
    site: str | None = None,
    device_name: str | None = None,
) -> dict[str, Any]:
    """List indexed source files and metadata without semantic search."""
    return SERVICE.list_sources(
        doc_type=doc_type,
        service=service,
        status=status,
        site=site,
        device_name=device_name,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
