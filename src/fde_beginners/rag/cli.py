import argparse
import json
from pathlib import Path

from fde_beginners.ai.provider_factory import create_provider
from fde_beginners.common.logging import configure_logging
from fde_beginners.rag.evaluation import evaluate, load_cases
from fde_beginners.rag.retrieval import CORPUS, Retriever, load_documents
from fde_beginners.rag.workflow import answer


def main() -> None:
    parser = argparse.ArgumentParser(description="Local Northstar policy retrieval and evaluation")
    parser.add_argument("command", choices=["ask", "evaluate"])
    parser.add_argument("--query", default="What is the return window with a receipt?")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--corpus", type=Path, default=CORPUS)
    parser.add_argument("--report", type=Path, help="Write per-case evaluation JSON to this path")
    parser.add_argument("--chunk-words", type=int, default=60)
    parser.add_argument("--audience", choices=["retail", "business", "all"], default="retail")
    parser.add_argument(
        "--failure",
        choices=[
            "normal",
            "drop_relevant",
            "stale_first",
            "wrong_policy",
            "no_context",
            "ignore_metadata",
        ],
        default="normal",
    )
    args = parser.parse_args()
    configure_logging()
    retriever, provider = (
        Retriever(load_documents(args.corpus), args.chunk_words),
        create_provider(),
    )
    if args.command == "evaluate":
        report = evaluate(retriever, provider, load_cases())
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({key: value for key, value in report.items() if key != "cases"}, indent=2))
    else:
        print(
            answer(
                retriever,
                provider,
                args.query,
                args.top_k,
                audience=args.audience,
                failure=args.failure,
            ).model_dump_json(indent=2)
        )
