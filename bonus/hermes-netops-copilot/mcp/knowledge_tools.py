from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import bootstrap  # noqa: F401

from netops_rag.config import get_settings
from netops_rag.documents import iter_documents
from netops_rag.filters import build_where_filter
from netops_rag.retriever import retrieve


@dataclass
class KnowledgeService:
    def _settings(self):
        return get_settings()

    def _source_root(self) -> Path:
        return self._settings().source_data_path

    def search(
        self,
        query: str,
        top_k: int = 5,
        device_name: str | None = None,
        site: str | None = None,
        doc_type: str | None = None,
        service: str | None = None,
        status: str | None = None,
        source_authority: str | None = None,
    ) -> dict[str, Any]:
        settings = self._settings()
        where = build_where_filter(
            device_name=[device_name] if device_name else None,
            site=[site] if site else None,
            doc_type=[doc_type] if doc_type else None,
            service=[service] if service else None,
            status=[status] if status else None,
            source_authority=[source_authority] if source_authority else None,
        )
        hits = retrieve(query, settings, top_k=top_k, where=where)
        return {
            "query": query,
            "filters": where or {},
            "hit_count": len(hits),
            "hits": [
                {
                    "source": hit.metadata.get("source"),
                    "metadata": hit.metadata,
                    "distance": hit.distance,
                    "content": hit.content,
                }
                for hit in hits
            ],
        }

    def list_sources(
        self,
        doc_type: str | None = None,
        service: str | None = None,
        status: str | None = None,
        site: str | None = None,
        device_name: str | None = None,
    ) -> dict[str, Any]:
        settings = self._settings()
        data_root = settings.source_data_path
        docs = iter_documents(data_root)
        rows = []
        for doc in docs:
            md = doc.metadata
            tests = [
                doc_type is None or md.get("doc_type") == doc_type,
                service is None or md.get("service") == service,
                status is None or md.get("status") == status,
                site is None or md.get("site") == site,
                device_name is None or md.get("device_name") == device_name,
            ]
            if all(tests):
                rows.append({"source": md.get("source"), "metadata": md})
        rows.sort(key=lambda item: str(item["source"]))
        return {"count": len(rows), "sources": rows}


SERVICE = KnowledgeService()
