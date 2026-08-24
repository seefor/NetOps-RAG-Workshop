from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from rich.console import Console

from netops_rag.config import Settings
from netops_rag.documents import Chunk, chunk_text, load_documents
from netops_rag.embeddings import get_embedding_client
from netops_rag.vectorstore import get_collection, reset_collection

console = Console()


def _chunk_id(source: str, index: int, text: str) -> str:
    digest = sha256(f"{source}:{index}:{text[:80]}".encode("utf-8")).hexdigest()[:16]
    return f"{Path(source).stem}-{index}-{digest}"


def build_chunks(data_dir: Path, settings: Settings) -> list[Chunk]:
    documents = load_documents(data_dir)
    chunks: list[Chunk] = []
    for doc in documents:
        doc_chunks = chunk_text(doc.text, settings.chunk_size, settings.chunk_overlap)
        for index, text in enumerate(doc_chunks):
            metadata = dict(doc.metadata)
            metadata["chunk_index"] = index
            metadata["chunk_count"] = len(doc_chunks)
            chunks.append(
                Chunk(
                    id=_chunk_id(str(doc.path.as_posix()), index, text),
                    text=text,
                    metadata=metadata,
                )
            )
    return chunks


def ingest(data_dir: Path, settings: Settings, reset: bool = False, batch_size: int = 64) -> int:
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than 0")
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory does not exist: {data_dir}")

    if reset:
        reset_collection(settings)

    collection = get_collection(settings)
    embedder = get_embedding_client(settings)
    chunks = build_chunks(data_dir, settings)

    if not chunks:
        console.print(f"[yellow]No supported documents found in {data_dir}[/yellow]")
        return 0

    console.print(f"Indexing {len(chunks)} chunks from {data_dir}...")
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        texts = [chunk.text for chunk in batch]
        embeddings = embedder.embed_texts(texts)
        if len(embeddings) != len(batch):
            raise RuntimeError(
                f"Embedding provider returned {len(embeddings)} vectors for {len(batch)} chunks"
            )
        if any(not vector for vector in embeddings):
            raise RuntimeError("Embedding provider returned an empty embedding vector")
        collection.upsert(
            ids=[chunk.id for chunk in batch],
            documents=texts,
            embeddings=embeddings,
            metadatas=[chunk.metadata for chunk in batch],
        )
        console.print(f"  indexed chunks {start + 1}-{start + len(batch)}")

    console.print(f"[green]Done. Indexed {len(chunks)} chunks.[/green]")
    return len(chunks)
