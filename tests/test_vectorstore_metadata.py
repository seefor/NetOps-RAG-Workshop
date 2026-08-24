from __future__ import annotations
import sys, types, unittest
sys.modules.setdefault("chromadb", types.ModuleType("chromadb"))
from netops_rag.config import Settings
from netops_rag.vectorstore import _validate_embedding_metadata
class FakeCollection:
    def __init__(self, metadata, count): self.metadata=metadata; self._count=count
    def count(self): return self._count
class VectorStoreMetadataTests(unittest.TestCase):
    def setUp(self): self.settings=Settings(embeddings_provider="ollama", ollama_embed_model="embeddinggemma")
    def test_legacy_populated_collection_requires_rebuild(self):
        with self.assertRaisesRegex(RuntimeError,"predates embedding-model tracking"): _validate_embedding_metadata(FakeCollection({},5),self.settings)
    def test_empty_legacy_collection_is_allowed(self): _validate_embedding_metadata(FakeCollection({},0),self.settings)
    def test_embedding_model_mismatch_is_explicit(self):
        collection=FakeCollection({"netops_embedding_provider":"ollama","netops_embedding_model":"all-minilm"},5)
        with self.assertRaisesRegex(RuntimeError,"Embedding configuration mismatch"): _validate_embedding_metadata(collection,self.settings)
if __name__ == "__main__": unittest.main()
