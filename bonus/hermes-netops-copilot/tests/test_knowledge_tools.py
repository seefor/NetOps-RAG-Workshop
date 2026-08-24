from __future__ import annotations

from pathlib import Path
import sys
import unittest

BONUS=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BONUS/"mcp"))
from knowledge_tools import KnowledgeService

class KnowledgeToolTests(unittest.TestCase):
    def test_lists_bgp_sources(self) -> None:
        service=KnowledgeService(); result=service.list_sources(service="bgp"); self.assertGreaterEqual(result["count"],5)
        sources={item["source"] for item in result["sources"]}; self.assertIn("data/runbooks/bgp-neighbor-down.md",sources)
    def test_filters_device_config(self) -> None:
        service=KnowledgeService(); result=service.list_sources(doc_type="config",device_name="nyc-edge-r1"); self.assertEqual(result["count"],1)

if __name__ == "__main__": unittest.main()
