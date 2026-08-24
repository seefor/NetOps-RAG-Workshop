from __future__ import annotations

from abc import ABC, abstractmethod

import requests

from netops_rag.config import Settings


class EmbeddingClient(ABC):
    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    def embed_query(self, text: str) -> list[float]:
        embeddings = self.embed_texts([text])
        if not embeddings:
            raise RuntimeError("Embedding provider returned no query embedding")
        return embeddings[0]


class OllamaEmbeddingClient(EmbeddingClient):
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = requests.post(
            f"{self.base_url}/api/embed",
            json={"model": self.model, "input": texts},
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        embeddings = data.get("embeddings") or []
        if len(embeddings) != len(texts):
            raise RuntimeError(
                f"Ollama returned {len(embeddings)} embeddings for {len(texts)} inputs: {data}"
            )
        return embeddings


class OpenAIEmbeddingClient(EmbeddingClient):
    def __init__(self, api_key: str | None, model: str) -> None:
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.client.embeddings.create(model=self.model, input=texts)
        ordered = [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
        if len(ordered) != len(texts):
            raise RuntimeError(
                f"OpenAI returned {len(ordered)} embeddings for {len(texts)} inputs"
            )
        return ordered


def get_embedding_client(settings: Settings) -> EmbeddingClient:
    if settings.embeddings_provider == "ollama":
        return OllamaEmbeddingClient(settings.ollama_base_url, settings.ollama_embed_model)
    if settings.embeddings_provider == "openai":
        return OpenAIEmbeddingClient(settings.openai_api_key, settings.openai_embed_model)
    raise ValueError("Unsupported EMBEDDINGS_PROVIDER. Use ollama or openai.")
