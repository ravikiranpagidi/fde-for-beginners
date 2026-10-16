import logging
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from fde_beginners.ai.provider import LLMProvider
from fde_beginners.ai.provider_factory import create_provider
from fde_beginners.common.logging import event
from fde_beginners.integration.client import OrderClient
from fde_beginners.integration.models import Order
from fde_beginners.northstar.data import Customer, OrderDetails
from fde_beginners.rag.retrieval import AS_OF, Hit, Retriever, load_documents
from fde_beginners.rag.workflow import answer
from fde_beginners.reliability.errors import IntegrationError
from fde_beginners.safe_tools.approval import TicketRequest

logger = logging.getLogger(__name__)
Fault = Literal[
    "normal",
    "order_timeout",
    "order_429",
    "order_unavailable",
    "policy_unavailable",
    "stale_policy",
    "malformed_customer",
]


class AssistRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)
    customer_id: str = Field(default="C001", pattern=r"^C[0-9]{3}$")
    order_id: str = Field(default="O100", pattern=r"^O[0-9]{3}$")
    question: str = Field(
        default="What is the return window with a receipt?", min_length=3, max_length=500
    )
    fault: Fault = "normal"


class Assistance(BaseModel):
    answer: str = "Insufficient evidence. Use the manual support workflow."
    sources: list[str] = Field(default_factory=list)
    customer: Customer | None = None
    order: Order | None = None
    order_details: OrderDetails | None = None
    decision_support: str = "Human review required; no eligibility decision was made."
    limitations: list[str] = Field(default_factory=list)
    suggested_action: str = "manual_review"
    requires_approval: bool = True
    state: str = "abstained"
    consulted: list[str] = Field(default_factory=list)
    evidence: list[Hit] = Field(default_factory=list)
    prior_ticket_ids: list[str] = Field(default_factory=list)
    error_code: str | None = None
    attempts: int | None = None


class SupportWorkflow:
    def __init__(
        self,
        data: dict,
        orders: OrderClient,
        *,
        provider: LLMProvider | None = None,
        retriever: Retriever | None = None,
    ):
        self.data, self.orders = data, orders
        self.provider = provider or create_provider()
        self.retriever = retriever or Retriever(load_documents())

    def assist(self, request: AssistRequest) -> Assistance:
        result = Assistance()
        event(logger, "request_started")

        def fallback(reason: str, state: str = "abstained") -> Assistance:
            result.state = state
            result.limitations.append(reason)
            event(logger, "fallback_selected", reason=reason, state=state)
            return result

        result.consulted.append("customer")
        event(logger, "customer_lookup")
        raw = self.data["customers"].get(request.customer_id)
        if raw is None:
            return fallback("customer_missing")
        if request.fault == "malformed_customer":
            raw = {**raw, "audience": 42}
        try:
            customer = Customer.model_validate(raw)
        except ValidationError:
            return fallback("customer_invalid")
        if customer.customer_id != request.customer_id:
            return fallback("customer_identity_mismatch", "restricted")
        # Local pilot boundary, not enterprise authentication or document ACLs.
        if customer.region != "US":
            return fallback("region_outside_pilot", "restricted")
        result.customer = customer
        result.consulted.append("order")
        event(logger, "order_lookup")
        modes = {
            "order_timeout": "timeout",
            "order_429": "rate_limit",
            "order_unavailable": "server_error",
        }
        try:
            order = self.orders.lookup(
                request.order_id,
                mode=modes.get(request.fault, "normal"),
                failures=3 if request.fault == "order_unavailable" else 1,
            )
        except IntegrationError as exc:
            result.error_code, result.attempts = exc.code, exc.attempts
            event(logger, "dependency_failed", code=exc.code, attempts=exc.attempts)
            return fallback("order_unavailable", "degraded")
        if order.customer_id != customer.customer_id or order.order_id != request.order_id:
            return fallback("order_customer_mismatch", "restricted")
        result.order = order
        result.attempts = self.orders.last_attempts
        try:
            result.order_details = OrderDetails.model_validate(
                self.data["order_details"].get(order.order_id)
            )
        except ValidationError:
            return fallback("order_details_invalid")
        result.consulted.append("tickets")
        result.prior_ticket_ids = [
            t["ticket_id"] for t in self.data["tickets"] if t["customer_id"] == customer.customer_id
        ]
        result.consulted.append("policy")
        if request.fault == "policy_unavailable":
            return fallback("policy_unavailable", "degraded")
        if customer.audience == "unknown":
            return fallback("policy_audience_ambiguous")
        try:
            rag = answer(
                self.retriever,
                self.provider,
                request.question,
                audience=customer.audience,
                failure="stale_first" if request.fault == "stale_policy" else "normal",
            )
        except ValueError:
            return fallback("invalid_model_evidence")
        result.evidence = rag.retrieved
        event(logger, "retrieval_complete", count=len(result.evidence))
        if any(h.effective > AS_OF or (h.expires and h.expires <= AS_OF) for h in rag.retrieved):
            return fallback("stale_policy_rejected")
        if rag.response.support == "insufficient":
            return fallback("insufficient_policy_evidence")
        result.answer = rag.response.answer
        result.sources = list(rag.response.citations)
        result.state = "drafted"
        result.suggested_action = "review_draft_and_optionally_create_ticket"
        result.limitations = [
            "Policy quotation only; representative must assess dates, condition, and exceptions.",
            "Ticket history is a read-only synthetic snapshot, not a live CRM.",
        ]
        event(logger, "draft_generated", citation_count=len(result.sources))
        return result


def prepare_ticket(result: Assistance, action_id: str) -> TicketRequest:
    """Application-owned payload. Model prose and suggested actions cannot set tool arguments."""
    if result.state != "drafted" or result.customer is None or result.order is None:
        raise ValueError("Only a validated draft can prepare a pilot ticket")
    request = TicketRequest(
        customer_id=result.customer.customer_id,
        summary=(
            f"Human review requested for order {result.order.order_id}; "
            f"policy sources: {', '.join(result.sources)}"
        ),
        action_id=action_id,
    )
    event(logger, "approval_requested")
    return request
