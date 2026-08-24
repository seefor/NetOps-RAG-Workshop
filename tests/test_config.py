import os
import unittest
from unittest.mock import patch
from netops_rag.config import Settings

class ConfigTests(unittest.TestCase):
    def test_settings_read_environment_at_instantiation(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "anthropic", "ANTHROPIC_API_KEY": "x"}):
            settings = Settings()
            self.assertEqual(settings.llm_provider, "anthropic")
    def test_invalid_overlap_is_rejected(self):
        settings = Settings(chunk_size=100, chunk_overlap=100)
        with self.assertRaises(ValueError):
            settings.validate()

if __name__ == "__main__":
    unittest.main()
