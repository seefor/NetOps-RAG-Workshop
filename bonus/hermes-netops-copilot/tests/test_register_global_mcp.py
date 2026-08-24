from __future__ import annotations

from pathlib import Path
import importlib.util
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"register_global_mcp.py"; spec=importlib.util.spec_from_file_location("register_global_mcp",SCRIPT); module=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module)

class RegisterGlobalMCPTests(unittest.TestCase):
    def test_expected_servers_are_read_only_and_use_active_python(self) -> None:
        servers=module.expected_servers(); self.assertEqual(set(servers),{"netops_rag","network_state"}); expected_python=str(Path(module.sys.executable).absolute())
        for server in servers.values():
            self.assertEqual(server["command"],expected_python); self.assertTrue(server["enabled"]); self.assertFalse(server["tools"]["prompts"]); self.assertFalse(server["tools"]["resources"])
        self.assertNotIn("configure_device",servers["network_state"]["tools"]["include"]); self.assertNotIn("push_config",servers["network_state"]["tools"]["include"])
    def test_mcp_add_command_puts_env_before_greedy_args(self) -> None:
        cfg=module.expected_servers()["netops_rag"]; cmd=module.mcp_add_command("hermes","netops_rag",cfg); self.assertLess(cmd.index("--env"),cmd.index("--args")); self.assertEqual(cmd[-1],cfg["args"][0])
    def test_same_workshop_server_accepts_old_workshop_path(self) -> None:
        wanted=module.expected_servers()["netops_rag"]; existing={"args":["/tmp/old/bonus/hermes-netops-copilot/mcp/netops_rag_server.py"]}; self.assertTrue(module.same_workshop_server(existing,wanted))

if __name__ == "__main__": unittest.main()
