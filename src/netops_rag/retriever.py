from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from netops_rag.config import Settings
from netops_rag.embeddings import get_embedding_client
from netops_rag.vectorstore import get_collection


@dataclass
class RetrievedChunk:
    id: str
    text: str
    metadata: dict[str, Any]
    distance: float | None = None


def retrieve(
    question: str,
    settings: Settings,
    top_k: int | None = None,
    where: dict[str, Any] | None = None,
) -> list[RetrievedChunk]:
    if not question.strip():
        raise ValueError("question must not be empty")

    collection = get_collection(settings)
    collection_count = collection.count()
    if collection_count == 0:
        return []

    requested_k = settings.top_k if top_k is None else top_k
    if requested_k <= 0:
        raise ValueError("top_k must be greater than 0")
    requested_k = min(requested_k, collection_count)

    embedder = get_embedding_client(settings)
    query_embedding = embedder.embed_query(question)
    query_args: dict[str, Any] = {
        "query_embeddings": [query_embedding],
        "n_results": requested_k,
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        query_args["where"] = where
    result = collection.query(**query_args)

    ids = result.get("ids", [[]])[0] or []
    documents = result.get("documents", [[]])[0] or []
    metadatas = result.get("metadatas", [[]])[0] or []
    distances = result.get("distances", [[]])[0] or []

    chunks: list[RetrievedChunk] = []
    for idx, doc, meta, distance in zip(ids, documents, metadatas, distances):
        if doc is None:
            continue
        chunks.append(
            RetrievedChunk(
                id=str(idx),
                text=str(doc),
                metadata=meta or {},
                distance=float(distance) if distance is not None else None,
            )
        )
    return chunks
