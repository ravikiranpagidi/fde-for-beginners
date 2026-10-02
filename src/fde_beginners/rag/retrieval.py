import json
import logging
import math
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from fde_beginners.common.logging import event
from fde_beginners.common.text import tokens

CORPUS = Path("labs/02-rag-and-evaluation/corpus.json")
AS_OF = date(2026, 10, 1)
logger = logging.getLogger(__name__)


class Document(BaseModel):
    source_id: str
    title: str
    topic: str
    audience: Literal["retail", "business", "all"]
    effective: date
    expires: date | None = None
    text: str = Field(min_length=1)

    @model_validator(mode="after")
    def dates_ordered(self) -> "Document":
        if self.expires and self.expires <= self.effective:
            raise ValueError("Expiry must follow effective date")
        return self


class Hit(BaseModel):
    source_id: str
    chunk_id: str
    text: str
    score: float
    title: str
    audience: str
    topic: str
    effective: date
    expires: date | None


def load_documents(path: Path = CORPUS) -> list[Document]:
    docs = [Document.model_validate(item) for item in json.loads(path.read_text(encoding="utf-8"))]
    if len({doc.source_id for doc in docs}) != len(docs):
        raise ValueError("Source IDs must be unique")
    return docs


def chunk_document(doc: Document, max_words: int = 60) -> list[Hit]:
    if max_words < 1:
        raise ValueError("Chunk size must be positive")
    chunks = []
    for paragraph in doc.text.split("\n\n"):
        words = paragraph.split()
        for start in range(0, len(words), max_words):
            chunks.append(
                Hit(
                    source_id=doc.source_id,
                    chunk_id=f"{doc.source_id}:{len(chunks)}",
                    text=" ".join(words[start : start + max_words]),
                    score=0,
                    title=doc.title,
                    audience=doc.audience,
                    topic=doc.topic,
                    effective=doc.effective,
                    expires=doc.expires,
                )
            )
    return chunks


class Retriever:
    def __init__(self, documents: list[Document], max_words: int = 60) -> None:
        self.chunks = [chunk for doc in documents for chunk in chunk_document(doc, max_words)]

    def search(
        self,
        query: str,
        k: int = 3,
        *,
        audience: str = "retail",
        as_of: date = AS_OF,
        ignore_metadata: bool = False,
        exclude: frozenset[str] = frozenset(),
    ) -> list[Hit]:
        if not 1 <= k <= 20:
            raise ValueError("top-k must be between 1 and 20")
        if audience not in {"retail", "business", "all"}:
            raise ValueError("Unknown audience")
        chunks = [
            c
            for c in self.chunks
            if c.source_id not in exclude
            and (
                ignore_metadata
                or (
                    c.effective <= as_of
                    and (c.expires is None or as_of < c.expires)
                    and (audience == "all" or c.audience in {audience, "all"})
                )
            )
        ]
        if not chunks:
            return []
        counts = [Counter(tokens(c.title + " " + c.text)) for c in chunks]
        average_length = sum(sum(count.values()) for count in counts) / len(counts)
        results = []
        for chunk, count in zip(chunks, counts, strict=True):
            score = 0.0
            for term in sorted(set(tokens(query))):
                frequency = count[term]
                document_frequency = sum(term in candidate for candidate in counts)
                idf = math.log(
                    1 + (len(chunks) - document_frequency + 0.5) / (document_frequency + 0.5)
                )
                denominator = frequency + 1.5 * (
                    0.25 + 0.75 * sum(count.values()) / max(average_length, 1)
                )
                score += idf * frequency * 2.5 / denominator
            if score > 0:
                results.append(chunk.model_copy(update={"score": round(score, 6)}))
        results.sort(key=lambda hit: (-hit.score, hit.chunk_id))
        event(logger, "retrieval_completed", candidates=len(chunks), returned=min(k, len(results)))
        return results[:k]
