from __future__ import annotations

from pathlib import Path
import sys
import unittest


BONUS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BONUS / "mcp"))

from network_state_tools import ScenarioStore


class MockToolTests(unittest.TestCase):
    def test_bgp_scenario_evidence(self) -> None:
        store = ScenarioStore(scenario_override="bgp-policy-drift")
        bgp = store.protocol_summary("nyc-edge-r1", "bgp")
        self.assertEqual(bgp["data"]["peers"][0]["state"], "Active")
        diff = store.config_diff("nyc-edge-r1")
        self.assertTrue(diff["data"]["drift_detected"])
        self.assertFalse(diff["data"]["change_control_match"])

    def test_ipsec_scenario_evidence(self) -> None:
        store = ScenarioStore(scenario_override="branch-ipsec")
        ipsec = store.protocol_summary("branch-r1", "ipsec")
        self.assertEqual(ipsec["data"]["ikev2_state"], "AUTH_FAILED")
        route = store.route("branch-r1", "203.0.113.10/32")
        self.assertTrue(route["data"][0]["selected"])

    def test_missing_device_is_explicit(self) -> None:
        store = ScenarioStore(scenario_override="bgp-policy-drift")
        result = store.device_facts("missing-r1")
        self.assertEqual(result["error"], "device_not_in_scenario")


if __name__ == "__main__":
    unittest.main()
