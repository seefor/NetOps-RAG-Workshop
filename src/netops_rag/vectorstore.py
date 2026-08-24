from __future__ import annotations

import chromadb

try:
    from chromadb.errors import NotFoundError as ChromaNotFoundError
except ImportError:  # pragma: no cover - compatibility with older/test stubs
    class ChromaNotFoundError(Exception):
        pass

from netops_rag.config import Settings


EMBEDDING_PROVIDER_KEY = "netops_embedding_provider"
EMBEDDING_MODEL_KEY = "netops_embedding_model"


def _expected_metadata(settings: Settings) -> dict[str, str]:
    return {
        EMBEDDING_PROVIDER_KEY: settings.embeddings_provider,
        EMBEDDING_MODEL_KEY: settings.embedding_model,
    }


def _validate_embedding_metadata(collection, settings: Settings) -> None:
    metadata = collection.metadata or {}
    stored_provider = metadata.get(EMBEDDING_PROVIDER_KEY)
    stored_model = metadata.get(EMBEDDING_MODEL_KEY)

    # Workshop versions before v0.5.0 did not record the embedding provider/model.
    # If a legacy collection already has records, fail clearly rather than waiting for
    # Chroma to surface an opaque dimension mismatch after a provider/model switch.
    if not stored_provider and not stored_model:
        if collection.count() > 0:
            raise RuntimeError(
                "The existing Chroma collection predates embedding-model tracking. "
                "Rebuild it once with: netops-rag ingest --data data --reset"
            )
        return

    if stored_provider != settings.embeddings_provider or stored_model != settings.embedding_model:
        raise RuntimeError(
            "Embedding configuration mismatch: collection "
            f"'{settings.collection_name}' was indexed with {stored_provider}/{stored_model}, "
            f"but the current configuration is {settings.embeddings_provider}/{settings.embedding_model}. "
            "Run: netops-rag ingest --data data --reset"
        )


def get_collection(settings: Settings):
    client = chromadb.PersistentClient(path=str(settings.chroma_path))
    collection = client.get_or_create_collection(
        name=settings.collection_name,
        metadata=_expected_metadata(settings),
        # The workshop generates embeddings itself. Explicitly disabling Chroma's default
        # embedding function avoids an unnecessary second model and accidental re-embedding.
        embedding_function=None,
    )
    _validate_embedding_metadata(collection, settings)
    return collection


def reset_collection(settings: Settings) -> None:
    client = chromadb.PersistentClient(path=str(settings.chroma_path))
    try:
        client.delete_collection(settings.collection_name)
    except (ValueError, ChromaNotFoundError):
        # Chroma versions have surfaced missing collections as either ValueError
        # or NotFoundError. Reset must be safe on a brand-new workshop install.
        pass
    client.get_or_create_collection(
        name=settings.collection_name,
        metadata=_expected_metadata(settings),
        embedding_function=None,
    )
