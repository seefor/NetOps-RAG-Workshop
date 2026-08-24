from __future__ import annotations

from pathlib import Path
import importlib.util
import os
import tempfile
import unittest
from unittest.mock import patch

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"desktop_profile_setup.py"
spec=importlib.util.spec_from_file_location("desktop_profile_setup",SCRIPT); module=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module)

class DesktopProfileSetupTests(unittest.TestCase):
    def test_profile_config_sets_cwd_and_skills_without_workshop_mcp(self) -> None:
        config=module.build_profile_config(); self.assertIn("terminal",config); self.assertIn("skills",config); self.assertNotIn("mcp_servers",config); self.assertTrue(config["skills"]["write_approval"])
    def test_deep_merge_removes_only_stale_workshop_mcp(self) -> None:
        existing={"mcp_servers":{"other":{"command":"x"},"netops_rag":{"command":"old"},"network_state":{"command":"old"}},"skills":{"external_dirs":["/existing"]},"terminal":{"timeout":10}}
        merged=module.deep_merge_profile(existing,module.build_profile_config()); self.assertIn("other",merged["mcp_servers"]); self.assertNotIn("netops_rag",merged["mcp_servers"]); self.assertNotIn("network_state",merged["mcp_servers"]); self.assertIn("/existing",merged["skills"]["external_dirs"]); self.assertEqual(merged["terminal"]["timeout"],10); self.assertIn("cwd",merged["terminal"])
    def test_profile_home_uses_hermes_home_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ,{"HERMES_HOME":tmp}):
                self.assertEqual(module.profile_home("default"),Path(tmp).absolute()); self.assertEqual(module.profile_home("netops-workshop"),Path(tmp).absolute()/"profiles"/"netops-workshop")

if __name__ == "__main__": unittest.main()
