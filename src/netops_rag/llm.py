from __future__ import annotations

from abc import ABC, abstractmethod

import requests

from netops_rag.config import Settings


class LLMClient(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class OllamaLLMClient(LLMClient):
    def __init__(self, base_url: str, model: str, temperature: float = 0.1) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "options": {"temperature": self.temperature},
        }
        response = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=180)
        response.raise_for_status()
        data = response.json()
        text = data.get("message", {}).get("content", "").strip()
        if not text:
            raise RuntimeError(f"Ollama returned an empty chat response: {data}")
        return text


class OpenAILLMClient(LLMClient):
    def __init__(self, api_key: str | None, model: str) -> None:
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = response.choices[0].message.content or ""
        if not text.strip():
            raise RuntimeError("OpenAI returned an empty chat response")
        return text.strip()


class AnthropicLLMClient(LLMClient):
    def __init__(self, api_key: str | None, model: str, temperature: float = 0.1, max_tokens: int = 1200) -> None:
        from anthropic import Anthropic

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        parts: list[str] = []
        for block in response.content:
            text = getattr(block, "text", None)
            if text:
                parts.append(text)
        result = "\n".join(parts).strip()
        if not result:
            raise RuntimeError("Anthropic returned an empty message response")
        return result


def get_llm_client(settings: Settings) -> LLMClient:
    if settings.llm_provider == "ollama":
        return OllamaLLMClient(settings.ollama_base_url, settings.ollama_chat_model, settings.temperature)
    if settings.llm_provider == "openai":
        return OpenAILLMClient(settings.openai_api_key, settings.openai_chat_model)
    if settings.llm_provider == "anthropic":
        return AnthropicLLMClient(settings.anthropic_api_key, settings.anthropic_model, settings.temperature, settings.max_tokens)
    raise ValueError("Unsupported LLM_PROVIDER")
