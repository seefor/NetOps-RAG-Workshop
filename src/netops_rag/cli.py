from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config import get_settings
from .documents import chunk_text, load_documents
from .filters import build_where_filter

console = Console()

FILTER_FIELDS = ("device", "site", "doc_type", "service", "status", "source_authority")


def _where_from_args(args: argparse.Namespace) -> dict[str, Any] | None:
    raw = {
        "device_name": getattr(args, "device", None),
        "site": getattr(args, "site", None),
        "doc_type": getattr(args, "doc_type", None),
        "service": getattr(args, "service", None),
        "status": getattr(args, "status", None),
        "source_authority": getattr(args, "source_authority", None),
    }
    return build_where_filter(raw)


def _add_filter_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--device", action="append", help="Filter by device_name; repeat for OR")
    parser.add_argument("--site", action="append", help="Filter by site; repeat for OR")
    parser.add_argument("--doc-type", action="append", help="Filter by doc_type; repeat for OR")
    parser.add_argument("--service", action="append", help="Filter by service; repeat for OR")
    parser.add_argument("--status", action="append", help="Filter by status; repeat for OR")
    parser.add_argument(
        "--source-authority",
        action="append",
        help="Filter by source_authority; repeat for OR",
    )


def cmd_ingest(args: argparse.Namespace) -> None:
    from .ingest import ingest

    settings = get_settings()
    ingest(Path(args.data), settings, reset=args.reset)


def cmd_ask(args: argparse.Namespace) -> None:
    from .rag import answer_question

    settings = get_settings()
    where = _where_from_args(args)
    answer, sources = answer_question(args.question, settings, where=where)
    console.print(Panel(answer, title="NetOps RAG Answer", expand=False))

    table = Table(title="Retrieved Sources")
    for heading in ["Label", "Source", "Type", "Service", "Status", "Authority", "Distance"]:
        table.add_column(heading)
    for index, chunk in enumerate(sources, start=1):
        table.add_row(
            f"S{index}",
            str(chunk.metadata.get("source", "unknown")),
            str(chunk.metadata.get("doc_type", "unknown")),
            str(chunk.metadata.get("service", "unknown")),
            str(chunk.metadata.get("status", "unknown")),
            str(chunk.metadata.get("source_authority", "unknown")),
            f"{chunk.distance:.4f}" if chunk.distance is not None else "n/a",
        )
    console.print(table)
    if where:
        console.print(f"[dim]metadata filter={where}[/dim]")


def cmd_retrieve(args: argparse.Namespace) -> None:
    from .retriever import retrieve

    settings = get_settings()
    where = _where_from_args(args)
    chunks = retrieve(args.question, settings, top_k=args.top_k, where=where)
    for index, chunk in enumerate(chunks, start=1):
        console.rule(f"S{index}: {chunk.metadata.get('source', 'unknown')}")
        console.print(chunk.text[: args.preview_chars])
        console.print(f"[dim]metadata={chunk.metadata} distance={chunk.distance}[/dim]")
    if where:
        console.print(f"[dim]metadata filter={where}[/dim]")


def _matches(doc_meta: dict[str, Any], args: argparse.Namespace) -> bool:
    mappings = {
        "doc_type": getattr(args, "doc_type", None),
        "service": getattr(args, "service", None),
        "status": getattr(args, "status", None),
        "site": getattr(args, "site", None),
    }
    return all(not values or str(doc_meta.get(key, "")) in values for key, values in mappings.items())


def cmd_catalog(args: argparse.Namespace) -> None:
    docs = [doc for doc in load_documents(Path(args.data)) if _matches(doc.metadata, args)]
    table = Table(title=f"NetOps Source Catalog ({len(docs)} documents)")
    for heading in ["File", "Type", "Service", "Device", "Site", "Status", "Authority"]:
        table.add_column(heading)
    for doc in docs:
        meta = doc.metadata
        table.add_row(
            str(meta.get("source", doc.path.as_posix())),
            str(meta.get("doc_type", "")),
            str(meta.get("service", "")),
            str(meta.get("device_name", "")),
            str(meta.get("site", "")),
            str(meta.get("status", "")),
            str(meta.get("source_authority", "")),
        )
    console.print(table)


def cmd_stats(args: argparse.Namespace) -> None:
    settings = get_settings()
    docs = load_documents(Path(args.data))
    chunk_count = sum(
        len(chunk_text(doc.text, settings.chunk_size, settings.chunk_overlap)) for doc in docs
    )
    console.print(
        Panel(f"Documents: {len(docs)}\nChunks: {chunk_count}", title="Dataset Stats")
    )
    for field in ["doc_type", "service", "status", "vendor", "site"]:
        counts = Counter(str(doc.metadata.get(field, "unknown")) for doc in docs)
        table = Table(title=field)
        table.add_column("Value")
        table.add_column("Documents", justify="right")
        for value, count in counts.most_common():
            table.add_row(value, str(count))
        console.print(table)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NetOps RAG Workshop CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest_parser = sub.add_parser("ingest", help="Ingest NetOps docs into Chroma")
    ingest_parser.add_argument("--data", default="data", help="Data directory to index")
    ingest_parser.add_argument("--reset", action="store_true", help="Reset collection first")
    ingest_parser.set_defaults(func=cmd_ingest)

    ask_parser = sub.add_parser("ask", help="Ask the NetOps RAG assistant")
    ask_parser.add_argument("question")
    _add_filter_arguments(ask_parser)
    ask_parser.set_defaults(func=cmd_ask)

    retrieve_parser = sub.add_parser("retrieve", help="Show retrieved chunks without generation")
    retrieve_parser.add_argument("question")
    retrieve_parser.add_argument("--top-k", type=int, default=None)
    retrieve_parser.add_argument("--preview-chars", type=int, default=800)
    _add_filter_arguments(retrieve_parser)
    retrieve_parser.set_defaults(func=cmd_retrieve)

    catalog_parser = sub.add_parser("catalog", help="List source documents and metadata")
    catalog_parser.add_argument("--data", default="data")
    catalog_parser.add_argument("--doc-type", action="append")
    catalog_parser.add_argument("--service", action="append")
    catalog_parser.add_argument("--status", action="append")
    catalog_parser.add_argument("--site", action="append")
    catalog_parser.set_defaults(func=cmd_catalog)

    stats_parser = sub.add_parser("stats", help="Show document and chunk statistics")
    stats_parser.add_argument("--data", default="data")
    stats_parser.set_defaults(func=cmd_stats)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
