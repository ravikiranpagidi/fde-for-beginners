"""A lexical extractive fixture, not a simulation of model intelligence."""

import hashlib
import re

from fde_beginners.ai.models import LLMRequest, LLMResponse
from fde_beginners.common.text import tokens


class MockLLMProvider:
    def generate(self, request: LLMRequest) -> LLMResponse:
        digest = hashlib.sha256(request.model_dump_json().encode()).hexdigest()[:16]
        query = set(tokens(request.user_input))
        candidates = []
        for record in request.context:
            for sentence in re.split(r"(?<=[.!?])\s+", record.text):
                overlap = len(query & set(tokens(sentence)))
                candidates.append((overlap, record.source_id, sentence))
        candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
        if not candidates or candidates[0][0] < 2:
            return LLMResponse(
                answer="Insufficient evidence. Ask a policy reviewer.",
                support="insufficient",
                request_digest=digest,
                structured_content={"reason": "fewer_than_two_matching_terms"},
            )
        _, source, sentence = candidates[0]
        return LLMResponse(
            answer=sentence,
            citations=(source,),
            support="extractive",
            request_digest=digest,
            structured_content={"method": "highest_lexical_overlap"},
        )
