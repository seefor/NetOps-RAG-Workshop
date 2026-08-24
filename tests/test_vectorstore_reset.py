from __future__ import annotations
import sys, types, unittest
chromadb = sys.modules.setdefault("chromadb", types.ModuleType("chromadb"))
errors = sys.modules.setdefault("chromadb.errors", types.ModuleType("chromadb.errors"))
class NotFoundError(Exception): pass
errors.NotFoundError = NotFoundError
from netops_rag.config import Settings
import netops_rag.vectorstore as vectorstore

class FakeClient:
    def __init__(self, delete_error=None): self.delete_error=delete_error; self.created=False
    def delete_collection(self, name):
        if self.delete_error is not None: raise self.delete_error
    def get_or_create_collection(self, **kwargs): self.created=True; return object()

class ResetCollectionTests(unittest.TestCase):
    def setUp(self): self.settings=Settings()
    def _run_with_client(self, client):
        old=getattr(chromadb,"PersistentClient",None); chromadb.PersistentClient=lambda **kwargs: client
        try: vectorstore.reset_collection(self.settings)
        finally:
            if old is None: delattr(chromadb,"PersistentClient")
            else: chromadb.PersistentClient=old
    def test_reset_ignores_not_found_error(self):
        client=FakeClient(vectorstore.ChromaNotFoundError("missing")); self._run_with_client(client); self.assertTrue(client.created)
    def test_reset_ignores_value_error_for_older_chroma(self):
        client=FakeClient(ValueError("missing")); self._run_with_client(client); self.assertTrue(client.created)
    def test_reset_recreates_after_successful_delete(self):
        client=FakeClient(); self._run_with_client(client); self.assertTrue(client.created)

if __name__ == "__main__": unittest.main()
