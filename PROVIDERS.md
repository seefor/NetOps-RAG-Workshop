# Provider Guide

The workshop separates answer generation from embeddings.

## Ollama default

```env
LLM_PROVIDER=ollama
EMBEDDINGS_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama3.2
OLLAMA_EMBED_MODEL=embeddinggemma
```

This path keeps both the answer model and embeddings local.

## OpenAI

```env
LLM_PROVIDER=openai
EMBEDDINGS_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_CHAT_MODEL=gpt-5-mini
OPENAI_EMBED_MODEL=text-embedding-3-small
```

Changing the embedding provider or embedding model requires rebuilding the Chroma collection.

## Anthropic with local embeddings

```env
LLM_PROVIDER=anthropic
EMBEDDINGS_PROVIDER=ollama
ANTHROPIC_API_KEY=...
ANTHROPIC_MODEL=claude-sonnet-5
```

Anthropic is used only for answer generation in this workshop starter stack. Ollama or OpenAI supplies embeddings.

## Workshop guidance

Provider switching is useful for comparing latency, answer style, and model behavior. It is not the main retrieval-quality lever. Inspect source quality, metadata, chunking, and retrieved evidence before changing the model.
