from __future__ import annotations

from pathlib import Path

import yaml
from rich.console import Console
from rich.table import Table

from netops_rag.config import PROJECT_ROOT, get_settings
from netops_rag.rag import answer_question

console = Console()


def run_eval(path: Path | None = None) -> None:
    eval_path = path or (PROJECT_ROOT / "evals" / "questions.yaml")
    settings = get_settings()
    questions = yaml.safe_load(eval_path.read_text(encoding="utf-8"))
    table = Table(title="NetOps RAG Evaluation")
    table.add_column("Question")
    table.add_column("Required Source")
    table.add_column("Observed Sources")
    table.add_column("Pass Hint")

    for item in questions:
        answer, sources = answer_question(item["question"], settings)
        observed = ", ".join(str(src.metadata.get("source", "unknown")) for src in sources)
        required = item.get("required_source", "")
        pass_hint = "✅" if required and required in observed else "review"
        table.add_row(item["question"], required, observed, pass_hint)
        console.rule(item["question"])
        console.print(answer)
    console.print(table)


if __name__ == "__main__":
    run_eval()
