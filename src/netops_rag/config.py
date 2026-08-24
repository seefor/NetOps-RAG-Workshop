from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return int(value)


def _float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return float(value)


def _project_path(name: str, default: str) -> Path:
    raw = Path(os.getenv(name, default)).expanduser()
    return raw if raw.is_absolute() else (PROJECT_ROOT / raw).resolve()


@dataclass(frozen=True)
class Settings:
    llm_provider: str = field(default_factory=lambda: _env("LLM_PROVIDER", "ollama").lower())
    embeddings_provider: str = field(
        default_factory=lambda: _env("EMBEDDINGS_PROVIDER", "ollama").lower()
    )

    ollama_base_url: str = field(
        default_factory=lambda: _env("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    )
    ollama_chat_model: str = field(default_factory=lambda: _env("OLLAMA_CHAT_MODEL", "llama3.2"))
    ollama_embed_model: str = field(
        default_factory=lambda: _env("OLLAMA_EMBED_MODEL", "embeddinggemma")
    )

    openai_api_key: str | None = field(default_factory=lambda: os.getenv("OPENAI_API_KEY") or None)
    openai_chat_model: str = field(default_factory=lambda: _env("OPENAI_CHAT_MODEL", "gpt-5-mini"))
    openai_embed_model: str = field(
        default_factory=lambda: _env("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    )

    anthropic_api_key: str | None = field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY") or None
    )
    anthropic_model: str = field(
        default_factory=lambda: _env("ANTHROPIC_MODEL", "claude-sonnet-5")
    )

    chroma_path: Path = field(default_factory=lambda: _project_path("CHROMA_PATH", ".chroma"))
    collection_name: str = field(
        default_factory=lambda: _env("COLLECTION_NAME", "netops_knowledge")
    )

    chunk_size: int = field(default_factory=lambda: _int("CHUNK_SIZE", 700))
    chunk_overlap: int = field(default_factory=lambda: _int("CHUNK_OVERLAP", 100))
    top_k: int = field(default_factory=lambda: _int("TOP_K", 5))
    temperature: float = field(default_factory=lambda: _float("TEMPERATURE", 0.1))
    max_tokens: int = field(default_factory=lambda: _int("MAX_TOKENS", 1200))

    @property
    def embedding_model(self) -> str:
        if self.embeddings_provider == "ollama":
            return self.ollama_embed_model
        return self.openai_embed_model

    def validate(self) -> None:
        if self.llm_provider not in {"ollama", "openai", "anthropic"}:
            raise ValueError("LLM_PROVIDER must be one of: ollama, openai, anthropic")
        if self.embeddings_provider not in {"ollama", "openai"}:
            raise ValueError("EMBEDDINGS_PROVIDER must be one of: ollama, openai")
        if self.llm_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        if self.embeddings_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when EMBEDDINGS_PROVIDER=openai")
        if self.llm_provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")
        if self.chunk_size <= 0:
            raise ValueError("CHUNK_SIZE must be greater than 0")
        if self.chunk_overlap < 0 or self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be >= 0 and smaller than CHUNK_SIZE")
        if self.top_k <= 0:
            raise ValueError("TOP_K must be greater than 0")
        if self.max_tokens <= 0:
            raise ValueError("MAX_TOKENS must be greater than 0")
        if self.temperature < 0:
            raise ValueError("TEMPERATURE must be >= 0")


def get_settings() -> Settings:
    settings = Settings()
    settings.validate()
    return settings
