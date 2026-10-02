import json
from pathlib import Path

from pydantic import BaseModel

from fde_beginners.ai.provider import LLMProvider
from fde_beginners.rag.retrieval import Retriever
from fde_beginners.rag.workflow import answer

GOLDEN = Path("labs/02-rag-and-evaluation/golden.json")


class Case(BaseModel):
    question: str
    expected_documents: list[str]
    expected_facts: list[str]
    should_abstain: bool = False
    audience: str = "retail"
    category: str


def document_ids(hits) -> list[str]:
    return list(dict.fromkeys(hit.source_id for hit in hits))


def recall_at_k(retrieved: list[str], expected: list[str], k: int) -> float:
    if not expected:
        raise ValueError("Recall is undefined for a case with no relevant documents")
    return len(set(retrieved[:k]) & set(expected)) / len(set(expected))


def reciprocal_rank(retrieved: list[str], expected: list[str]) -> float:
    return next((1 / rank for rank, doc in enumerate(retrieved, 1) if doc in expected), 0.0)


def evaluate(retriever: Retriever, provider: LLMProvider, cases: list[Case]) -> dict:
    if not cases:
        raise ValueError("Evaluation requires cases")
    recall1, recall3, ranks, rows = [], [], [], []
    for case in cases:
        result = answer(retriever, provider, case.question, 3, audience=case.audience)
        ids = document_ids(retriever.search(case.question, 20, audience=case.audience))[:3]
        if case.expected_documents:
            recall1.append(recall_at_k(ids, case.expected_documents, 1))
            recall3.append(recall_at_k(ids, case.expected_documents, 3))
            ranks.append(reciprocal_rank(ids, case.expected_documents))
        abstained = result.response.support == "insufficient"
        rows.append(
            {
                **case.model_dump(),
                "retrieved": ids,
                "answer_context": [h.model_dump(mode="json") for h in result.retrieved],
                "answer": result.response.answer,
                "citations": result.response.citations,
                "abstention_pass": abstained == case.should_abstain,
                "facts_pass": (
                    abstained
                    if case.should_abstain
                    else not abstained
                    and all(
                        f.lower() in result.response.answer.lower() for f in case.expected_facts
                    )
                ),
            }
        )

    def mean(values: list[float]) -> float | None:
        return round(sum(values) / len(values), 4) if values else None

    return {
        "questions": len(cases),
        "retrieval_cases": len(recall1),
        "k_unit": "unique_documents",
        "recall_at_1": mean(recall1),
        "recall_at_3": mean(recall3),
        "mrr_at_3": mean(ranks),
        "abstention_checks_passed": sum(r["abstention_pass"] for r in rows),
        "fact_checks_passed": sum(r["facts_pass"] for r in rows),
        "cases": rows,
    }


def load_cases(path: Path = GOLDEN) -> list[Case]:
    return [Case.model_validate(row) for row in json.loads(path.read_text(encoding="utf-8"))]
