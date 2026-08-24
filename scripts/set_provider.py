#!/usr/bin/env python3
"""Safely switch the workshop answer provider in .env."""

from __future__ import annotations

import argparse
from getpass import getpass
from pathlib import Path

DEFAULTS = {
    "ollama": {"LLM_PROVIDER": "ollama", "EMBEDDINGS_PROVIDER": "ollama"},
    "openai": {"LLM_PROVIDER": "openai", "EMBEDDINGS_PROVIDER": "ollama"},
    "anthropic": {"LLM_PROVIDER": "anthropic", "EMBEDDINGS_PROVIDER": "ollama"},
}


def parse_env(lines: list[str]) -> dict[str, str]:
    values = {}
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def update_lines(lines: list[str], updates: dict[str, str]) -> list[str]:
    remaining = dict(updates)
    output = []
    for raw in lines:
        stripped = raw.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in remaining:
                output.append(f"{key}={remaining.pop(key)}")
                continue
        output.append(raw)
    if remaining:
        output.append("")
        output.extend(f"{key}={value}" for key, value in remaining.items())
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Switch NetOps RAG workshop providers")
    parser.add_argument("provider", choices=["ollama", "openai", "anthropic"])
    parser.add_argument("--openai-embeddings", action="store_true", help="Use OpenAI embeddings as well as OpenAI answer generation")
    args = parser.parse_args()
    env_path = Path(".env")
    if not env_path.exists():
        example = Path(".env.example")
        if not example.exists():
            raise SystemExit("Neither .env nor .env.example exists.")
        env_path.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
    lines = env_path.read_text(encoding="utf-8").splitlines()
    current = parse_env(lines)
    updates = dict(DEFAULTS[args.provider])
    if args.provider == "openai":
        if args.openai_embeddings:
            updates["EMBEDDINGS_PROVIDER"] = "openai"
        if not current.get("OPENAI_API_KEY"):
            key = getpass("Enter OPENAI_API_KEY (input hidden): ").strip()
            if not key:
                raise SystemExit("An OpenAI API key is required for this provider.")
            updates["OPENAI_API_KEY"] = key
    if args.provider == "anthropic" and not current.get("ANTHROPIC_API_KEY"):
        key = getpass("Enter ANTHROPIC_API_KEY (input hidden): ").strip()
        if not key:
            raise SystemExit("An Anthropic API key is required for this provider.")
        updates["ANTHROPIC_API_KEY"] = key
    previous_embeddings = current.get("EMBEDDINGS_PROVIDER", "ollama").lower()
    new_embeddings = updates["EMBEDDINGS_PROVIDER"].lower()
    previous_model = current.get("OPENAI_EMBED_MODEL", "text-embedding-3-small") if previous_embeddings == "openai" else current.get("OLLAMA_EMBED_MODEL", "embeddinggemma")
    merged = dict(current); merged.update(updates)
    new_model = merged.get("OPENAI_EMBED_MODEL", "text-embedding-3-small") if new_embeddings == "openai" else merged.get("OLLAMA_EMBED_MODEL", "embeddinggemma")
    env_path.write_text("\n".join(update_lines(lines, updates)) + "\n", encoding="utf-8")
    print(f"Updated .env: LLM_PROVIDER={updates['LLM_PROVIDER']}")
    print(f"Updated .env: EMBEDDINGS_PROVIDER={updates['EMBEDDINGS_PROVIDER']}")
    if previous_embeddings != new_embeddings or previous_model != new_model:
        print("Embedding provider/model changed. Run: netops-rag ingest --data data --reset")
    else:
        print("Re-ingestion is not required because the embedding provider/model did not change.")
    print("Restart Streamlit if it is running so the application reloads .env.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
