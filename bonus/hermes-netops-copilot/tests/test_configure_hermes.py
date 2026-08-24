from __future__ import annotations

from pathlib import Path
import importlib.util
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "configure_hermes.py"
spec = importlib.util.spec_from_file_location("configure_hermes", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class ConfigTests(unittest.TestCase):
    def test_compatibility_builder_returns_both_servers(self) -> None:
        config = module.build_config()
        self.assertIn("netops_rag", config)
        self.assertIn("network_state", config)
        self.assertFalse(config["network_state"]["tools"]["resources"])


if __name__ == "__main__":
    unittest.main()
