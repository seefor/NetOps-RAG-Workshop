#!/usr/bin/env python3
"""Workshop preflight checks for the NetOps RAG stack."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import sys
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def report(ok: bool, label: str, detail: str = "") -> bool:
    status = "PASS" if ok else "FAIL"
    suffix = f" — {detail}" if detail else ""
    print(f"[{status}] {label}{suffix}")
    return ok


def main() -> int:
    all_ok = True
    all_ok &= report(sys.version_info >= (3, 10), "Python version", sys.version.split()[0])
    env_path = ROOT / ".env"
    env = load_env(env_path)
    all_ok &= report(env_path.exists(), ".env file", str(env_path))
    cli_path = shutil.which("netops-rag")
    all_ok &= report(cli_path is not None, "netops-rag command", cli_path or "not found")
    for package in ("chromadb", "dotenv", "requests", "rich", "yaml", "streamlit"):
        found = importlib.util.find_spec(package) is not None
        all_ok &= report(found, f"Python package: {package}")
    package_found = importlib.util.find_spec("netops_rag") is not None
    all_ok &= report(package_found, "netops_rag package import", "editable install expected")
    all_ok &= report((ROOT / "streamlit_app.py").exists(), "Streamlit entrypoint", "streamlit_app.py")
    llm_provider = env.get("LLM_PROVIDER", "ollama").lower()
    embeddings_provider = env.get("EMBEDDINGS_PROVIDER", "ollama").lower()
    report(True, "LLM provider", llm_provider)
    report(True, "Embeddings provider", embeddings_provider)
    if llm_provider == "openai" or embeddings_provider == "openai":
        all_ok &= report(importlib.util.find_spec("openai") is not None, "Python package: openai")
        all_ok &= report(bool(env.get("OPENAI_API_KEY")), "OPENAI_API_KEY")
    if llm_provider == "anthropic":
        all_ok &= report(importlib.util.find_spec("anthropic") is not None, "Python package: anthropic")
        all_ok &= report(bool(env.get("ANTHROPIC_API_KEY")), "ANTHROPIC_API_KEY")
    if llm_provider == "ollama" or embeddings_provider == "ollama":
        base_url = env.get("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        try:
            with urlopen(f"{base_url}/api/tags", timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
            models = [str(item.get("name", "")) for item in payload.get("models", [])]
            all_ok &= report(True, "Ollama API", base_url)
            def model_present(requested: str) -> bool:
                return any(name == requested or name.startswith(f"{requested}:") for name in models)
            if llm_provider == "ollama":
                chat_model = env.get("OLLAMA_CHAT_MODEL", "llama3.2")
                all_ok &= report(model_present(chat_model), f"Chat model: {chat_model}")
            if embeddings_provider == "ollama":
                embed_model = env.get("OLLAMA_EMBED_MODEL", "embeddinggemma")
                all_ok &= report(model_present(embed_model), f"Embedding model: {embed_model}")
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            all_ok &= report(False, "Ollama API", str(exc))
    data_dir = ROOT / "data"
    source_count = sum(1 for path in data_dir.rglob("*") if path.is_file()) if data_dir.exists() else 0
    all_ok &= report(data_dir.exists() and source_count > 0, "Workshop dataset", f"{source_count} files")
    print()
    if all_ok:
        print("Preflight passed. The workshop stack is ready.")
        print("Launch UI: python -m streamlit run streamlit_app.py")
        return 0
    print("Preflight found one or more problems. Fix the FAIL items and rerun this script.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
