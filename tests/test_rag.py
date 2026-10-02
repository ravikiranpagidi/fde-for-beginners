from datetime import date

import pytest

from fde_beginners.ai.models import LLMResponse
from fde_beginners.ai.provider_factory import create_provider
from fde_beginners.rag.evaluation import evaluate, load_cases, recall_at_k, reciprocal_rank
from fde_beginners.rag.retrieval import Retriever, chunk_document, load_documents
from fde_beginners.rag.workflow import answer, validate_citations


@pytest.fixture
def retriever():
    return Retriever(load_documents())


def test_retrieval_is_deterministic_and_top_k_bounded(retriever):
    one = retriever.search("return window receipt", 1)
    assert one == retriever.search("return window receipt", 1)
    assert len(one) == 1
    assert one[0].source_id == "returns-current"
    assert one[0].score > 0


def test_chunking_preserves_metadata_and_exposes_boundary_tradeoff():
    doc = load_documents()[0]
    chunks = chunk_document(doc, 4)
    assert all(c.source_id == doc.source_id and c.effective == doc.effective for c in chunks)
    assert all(len(c.text.split()) <= 4 for c in chunks)
    assert len({c.chunk_id for c in chunks}) == len(chunks)
    assert " ".join(c.text for c in chunks) == " ".join(doc.text.split())


@pytest.mark.parametrize("k", [0, -1, 21])
def test_invalid_k_rejected(retriever, k):
    with pytest.raises(ValueError, match="top-k"):
        retriever.search("return", k)


def test_metric_math_handles_misses_and_multiple_relevant_documents():
    assert recall_at_k(["a", "x", "b"], ["a", "b"], 1) == 0.5
    assert recall_at_k(["a", "x", "b"], ["a", "b"], 3) == 1
    assert reciprocal_rank(["x", "b"], ["a", "b"]) == 0.5
    assert reciprocal_rank(["x"], ["a"]) == 0
    with pytest.raises(ValueError):
        recall_at_k([], [], 3)


def test_current_metadata_filters_expired_future_and_other_audience(retriever):
    hits = retriever.search("return window receipt", 20)
    assert not {"00-returns-legacy", "holiday-future", "business-returns"} & {
        h.source_id for h in hits
    }
    older = retriever.search("return window receipt", 20, as_of=date(2025, 1, 1))
    assert {h.source_id for h in older} == {"00-returns-legacy"}


def test_known_answer_has_retrieved_citation(retriever):
    result = answer(retriever, create_provider(), "What is the return window with a receipt?")
    assert result.response.citations == ("returns-current",)
    assert "30 days" in result.response.answer
    validate_citations(result.response, result.retrieved)


@pytest.mark.parametrize("query", ["Lunar insurance?", "Can you promise my refund?"])
def test_insufficient_evidence_has_no_citations(retriever, query):
    result = answer(retriever, create_provider(), query)
    assert result.response.support == "insufficient"
    assert not result.response.citations


def test_conflicting_audience_abstains(retriever):
    result = answer(retriever, create_provider(), "return window receipt", audience="all")
    assert result.boundary == "ambiguous_audience"
    assert result.response.support == "insufficient"


def test_fabricated_citation_and_unsupported_extract_are_rejected(retriever):
    hits = retriever.search("return window receipt")
    response = LLMResponse(
        answer="Free refunds forever",
        citations=("invented",),
        support="extractive",
        request_digest="fixture",
    )
    with pytest.raises(ValueError, match="retrieved sources"):
        validate_citations(response, hits)
    with pytest.raises(ValueError, match="cited context"):
        validate_citations(response.model_copy(update={"citations": ("returns-current",)}), hits)


@pytest.mark.parametrize(
    "failure", ["drop_relevant", "stale_first", "wrong_policy", "no_context", "ignore_metadata"]
)
def test_failure_injection_exposes_context_or_metadata_problem(retriever, failure):
    result = answer(retriever, create_provider(), "return window receipt", failure=failure)
    if failure in {"drop_relevant", "wrong_policy"}:
        assert not result.retrieved or result.retrieved[0].source_id != "returns-current"
    elif failure == "stale_first":
        assert result.retrieved[0].source_id == "00-returns-legacy"
        assert "90 days" in result.response.answer
    elif failure == "no_context":
        assert not result.retrieved
        assert result.response.support == "insufficient"
    else:
        assert result.boundary in {"metadata_bypassed", "ambiguous_audience"}


def test_evaluation_is_reproducible_and_does_not_hide_failure(retriever):
    report = evaluate(retriever, create_provider(), load_cases())
    assert report == evaluate(retriever, create_provider(), load_cases())
    assert 0 < report["recall_at_3"] < 1
    mismatch = next(c for c in report["cases"] if c["category"] == "vocabulary_mismatch")
    assert not mismatch["facts_pass"]
    assert mismatch["retrieved"] == []


def test_bad_provider_output_fails_generation_boundary(retriever):
    class InvalidProvider:
        def generate(self, request):
            return LLMResponse(
                answer="Unbounded refunds",
                citations=("fake",),
                support="extractive",
                request_digest="fixture",
            )

    with pytest.raises(ValueError, match="retrieved sources"):
        answer(retriever, InvalidProvider(), "return window receipt")
