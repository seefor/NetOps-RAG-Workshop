from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml

SUPPORTED_EXTENSIONS = {".md", ".txt", ".cfg", ".conf", ".log"}


@dataclass
class SourceDocument:
    path: Path
    text: str
    metadata: dict[str, str | int | float | bool]


@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict[str, str | int | float | bool]


def _safe_metadata(value: Any) -> str | int | float | bool:
    if isinstance(value, (str, int, float, bool)):
        return value
    if value is None:
        return ""
    return str(value)


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    raw_meta, body = match.groups()
    parsed = yaml.safe_load(raw_meta) or {}
    if not isinstance(parsed, dict):
        parsed = {}
    return parsed, body


def _infer_doc_type(path: Path) -> str:
    parts = {part.lower() for part in path.parts}
    if "configs" in parts:
        return "config"
    if "runbooks" in parts:
        return "runbook"
    if "policies" in parts:
        return "policy"
    if "changes" in parts:
        return "change_record"
    if "incidents" in parts:
        return "incident"
    if "postmortems" in parts:
        return "postmortem"
    if "inventory" in parts:
        return "inventory"
    if "archive" in parts:
        return "archive"
    if "untrusted" in parts:
        return "untrusted"
    return "document"


def _infer_vendor_platform(path: Path, text: str) -> dict[str, str]:
    lower = (path.name + "\n" + text[:2000]).lower()
    if "pan-os" in lower or "palo alto" in lower or "set rulebase" in lower:
        return {"vendor": "paloalto", "platform": "pan-os"}
    if "router bgp" in lower or "ios-xe" in lower or "interface gigabitethernet" in lower:
        return {"vendor": "cisco", "platform": "ios-xe"}
    if "junos" in lower or "set protocols" in lower or "policy-statement" in lower:
        return {"vendor": "juniper", "platform": "junos"}
    if "arista" in lower or "management api http-commands" in lower:
        return {"vendor": "arista", "platform": "eos"}
    if "ltm pool" in lower or "ltm virtual" in lower:
        return {"vendor": "f5", "platform": "tmos"}
    return {}


def load_documents(data_dir: Path) -> list[SourceDocument]:
    docs: list[SourceDocument] = []
    for path in sorted(data_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        frontmatter, body = _parse_frontmatter(raw)
        inferred = _infer_vendor_platform(path, body)
        metadata: dict[str, Any] = {
            "source": str(path.as_posix()),
            "filename": path.name,
            "doc_type": _infer_doc_type(path),
            "relative_dir": str(path.parent.as_posix()),
            **inferred,
            **frontmatter,
        }
        safe_metadata = {key: _safe_metadata(value) for key, value in metadata.items()}
        docs.append(SourceDocument(path=path, text=body.strip(), metadata=safe_metadata))
    return docs


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Simple paragraph-aware chunker for the workshop.

    It keeps paragraph boundaries when possible and applies one consistent character
    overlap between final chunks. Long config stanzas are hard-split before overlap is
    applied. Production systems should replace this with format-aware parsing.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be >= 0 and smaller than chunk_size")
    if not text.strip():
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    base_chunks: list[str] = []
    current = ""

    for para in paragraphs:
        candidate = para if not current else f"{current}\n\n{para}"
        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            base_chunks.append(current)
            current = ""

        if len(para) <= chunk_size:
            current = para
            continue

        # Hard-split long paragraphs/config stanzas without overlap here. Overlap is
        # applied exactly once in the final pass below.
        for start in range(0, len(para), chunk_size):
            base_chunks.append(para[start : start + chunk_size])

    if current:
        base_chunks.append(current)

    if chunk_overlap == 0 or len(base_chunks) <= 1:
        return base_chunks

    final_chunks: list[str] = [base_chunks[0]]
    for index in range(1, len(base_chunks)):
        previous_tail = base_chunks[index - 1][-chunk_overlap:]
        room_for_current = max(1, chunk_size - len(previous_tail) - 2)
        current_body = base_chunks[index][:room_for_current]
        final_chunks.append(f"{previous_tail}\n\n{current_body}")
    return final_chunks
