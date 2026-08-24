from __future__ import annotations

import asyncio
from pathlib import Path
import sys

BONUS = Path(__file__).resolve().parents[1]
MCP_DIR = BONUS / "mcp"
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))

from mcp import Client
import mock_network_server
import netops_rag_server


async def check_server(name: str, server, expected_tool: str) -> None:
    async with Client(server) as client:
        tools_result = await client.list_tools()
        names = {tool.name for tool in tools_result.tools}
        if expected_tool not in names:
            raise RuntimeError(f"{name} missing expected tool {expected_tool}; got {sorted(names)}")
        print(f"{name}: {len(names)} tools available")


async def main() -> None:
    await check_server("netops_rag", netops_rag_server.mcp, "search_network_knowledge")
    await check_server("network_state", mock_network_server.mcp, "get_scenario_context")
    async with Client(mock_network_server.mcp) as client:
        result = await client.call_tool("get_scenario_context", {})
        if result.is_error:
            raise RuntimeError(f"network_state tool call returned an MCP error: {result.content}")
        print(f"network_state tool call returned structured content: {bool(result.structured_content)}")


if __name__ == "__main__":
    asyncio.run(main())
