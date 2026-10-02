from typing import Literal

from pydantic import BaseModel

from fde_beginners.ai.models import ContextRecord, LLMRequest, LLMResponse
from fde_beginners.ai.provider import LLMProvider
from fde_beginners.rag.retrieval import AS_OF, Hit, Retriever

Failure = Literal[
    "normal", "drop_relevant", "stale_first", "wrong_policy", "no_context", "ignore_metadata"
]


class RAGResult(BaseModel):
    question: str
    response: LLMResponse
    retrieved: list[Hit]
    boundary: str = "current_policy_filter"


def validate_citations(response: LLMResponse, hits: list[Hit]) -> None:
    sources = {hit.source_id: [] for hit in hits}
    for hit in hits:
        sources[hit.source_id].append(hit.text)
    if response.support == "insufficient":
        if response.citations:
            raise ValueError("Abstention must not contain citations")
        return
    if not response.citations or not set(response.citations) <= sources.keys():
        raise ValueError("Citations must reference retrieved sources")
    if not any(
        response.answer in text for source in response.citations for text in sources[source]
    ):
        raise ValueError("Extractive answer must occur in its cited context")


def answer(
    retriever: Retriever,
    provider: LLMProvider,
    question: str,
    k: int = 3,
    *,
    audience: str = "retail",
    as_of=AS_OF,
    failure: Failure = "normal",
) -> RAGResult:
    ignore = failure in {"ignore_metadata", "stale_first"}
    hits = retriever.search(
        "exchanges unopened item" if failure == "wrong_policy" else question,
        k,
        audience=audience,
        as_of=as_of,
        ignore_metadata=ignore,
        exclude=frozenset({"returns-current"}) if failure == "drop_relevant" else frozenset(),
    )
    if failure == "no_context":
        hits = []
    if failure == "stale_first":
        stale = retriever.search("return window receipt", 20, ignore_metadata=True)
        hits = [h for h in stale if h.source_id == "00-returns-legacy"][:1] + hits[: max(0, k - 1)]
    ambiguous = any(
        a.topic == b.topic
        and a.audience != b.audience
        and a.audience != "all"
        and b.audience != "all"
        for a in hits
        for b in hits
    )
    context = (
        () if ambiguous else tuple(ContextRecord(source_id=h.source_id, text=h.text) for h in hits)
    )
    response = provider.generate(LLMRequest(user_input=question, context=context))
    validate_citations(response, hits)
    return RAGResult(
        question=question,
        response=response,
        retrieved=hits,
        boundary="ambiguous_audience"
        if ambiguous
        else ("metadata_bypassed" if ignore else "current_policy_filter"),
    )
