from __future__ import annotations

from pathlib import Path
import json
import sys

BONUS=Path(__file__).resolve().parents[1]; MCP_DIR=BONUS/"mcp"
if str(MCP_DIR) not in sys.path: sys.path.insert(0,str(MCP_DIR))
from network_state_tools import ScenarioStore
from knowledge_tools import KnowledgeService

def main() -> None:
    store=ScenarioStore(); context=store.scenario_context(); devices=store.list_devices()
    print(json.dumps({"scenario":context,"devices":devices},indent=2))
    first=devices["devices"][0]["device_name"]; facts=store.device_facts(first)
    assert facts["synthetic"] is True and facts["read_only"] is True
    print(f"State tool smoke test passed for {first}.")
    knowledge=KnowledgeService(); catalog=knowledge.list_sources(service=context["service"]); assert catalog["count"]>0
    print(f"Knowledge catalog smoke test passed with {catalog['count']} matching sources.")

if __name__ == "__main__": main()
