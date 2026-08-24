from pathlib import Path
import tempfile, unittest
from netops_rag.documents import chunk_text, load_documents
class DocumentTests(unittest.TestCase):
    def test_frontmatter_and_doc_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"incidents"; p.mkdir(); (p/"INC-1.md").write_text("---\nservice: bgp\nstatus: resolved\n---\n# Incident\nBody",encoding="utf-8")
            docs=load_documents(Path(tmp)); self.assertEqual(len(docs),1); self.assertEqual(docs[0].metadata["doc_type"],"incident"); self.assertEqual(docs[0].metadata["service"],"bgp")
    def test_chunk_overlap_applied_once_and_size_is_bounded(self):
        text="A"*50+"\n\n"+"B"*50+"\n\n"+"C"*50; chunks=chunk_text(text,chunk_size=70,chunk_overlap=10)
        self.assertGreaterEqual(len(chunks),3); self.assertTrue(all(len(chunk)<=70 for chunk in chunks)); self.assertTrue(chunks[1].startswith("A"*10))
    def test_invalid_chunk_settings(self):
        with self.assertRaises(ValueError): chunk_text("hello",chunk_size=10,chunk_overlap=10)
        with self.assertRaises(ValueError): chunk_text("hello",chunk_size=0,chunk_overlap=0)
if __name__ == "__main__": unittest.main()
