import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from fde_beginners.northstar.data import PROJECT, load_data
from fde_beginners.northstar.runtime import local_orders
from fde_beginners.northstar.tickets import execute_ticket
from fde_beginners.northstar.workflow import AssistRequest, SupportWorkflow, prepare_ticket
from fde_beginners.rag.evaluation import document_ids, recall_at_k
from fde_beginners.safe_tools.approval import ApprovalStore


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    category: str
    request: AssistRequest
    expected_state: str
    expected_systems: list[str]
    expected_documents: list[str] = Field(default_factory=list)
    expected_fact: str | None = None
    expected_attempts: int | None = None
    expected_error: str | None = None
    write: Literal["none", "approved", "unapproved", "duplicate", "failure"] = "none"


async def evaluate() -> dict:
    cases = [
        Case.model_validate(row)
        for row in json.loads((PROJECT / "cases.json").read_text(encoding="utf-8"))
    ]
    if not cases:
        raise ValueError("Evaluation requires cases")
    data, rows = load_data(), []
    with TemporaryDirectory() as directory, local_orders(data) as orders:
        workflow = SupportWorkflow(data, orders)
        for case in cases:
            result = workflow.assist(case.request)
            ids = document_ids(result.evidence)
            checks = {
                "systems": result.consulted == case.expected_systems,
                "citation_membership": set(result.sources) <= set(ids),
                "citation_presence": bool(result.sources) == (result.state == "drafted"),
                "abstention": (result.state == "drafted") == bool(case.expected_fact),
                "fact": case.expected_fact is None
                or case.expected_fact.lower() in result.answer.lower(),
                "attempts": result.attempts == case.expected_attempts,
                "error": result.error_code == case.expected_error,
            }
            state, effect_count, writes = result.state, 0, []
            if case.write != "none":
                store = ApprovalStore(Path(directory) / f"{case.name}.db")
                prepared = prepare_ticket(result, case.name)
                token = None if case.write == "unapproved" else store.issue(prepared)
                writes.append(
                    await execute_ticket(data, store, prepared, token, fail=case.write == "failure")
                )
                state = writes[-1]["state"]
                if case.write == "duplicate":
                    # Replay is rejected; a fresh approval of the SAME action recovers its result.
                    writes.append(await execute_ticket(data, store, prepared, token))
                    writes.append(
                        await execute_ticket(data, store, prepared, store.issue(prepared))
                    )
                    checks["duplicate"] = (
                        writes[1]["state"] == "rejected"
                        and writes[2]["result"]["status"] == "existing"
                    )
                effect_count = store.ticket_count()
                checks["effects"] = effect_count == int(case.write in {"approved", "duplicate"})
            checks["state"] = state == case.expected_state
            rows.append(
                {
                    "name": case.name,
                    "category": case.category,
                    "expected_abstention": case.expected_fact is None,
                    "checks": checks,
                    "passed": all(checks.values()),
                    "state": state,
                    "effects": effect_count,
                    "recall_at_1": recall_at_k(ids, case.expected_documents, 1)
                    if case.expected_documents
                    else None,
                    "recall_at_3": recall_at_k(ids, case.expected_documents, 3)
                    if case.expected_documents
                    else None,
                    "assistance": result.model_dump(mode="json"),
                    "writes": writes,
                }
            )
    retrieval = [row for row in rows if row["recall_at_1"] is not None]
    return {
        "summary": {
            "cases": len(rows),
            "passed": sum(row["passed"] for row in rows),
            "retrieval_cases": len(retrieval),
            "k_unit": "unique_documents_in_actual_context",
            "recall_at_1": round(sum(row["recall_at_1"] for row in retrieval) / len(retrieval), 4)
            if retrieval
            else None,
            "recall_at_3": round(sum(row["recall_at_3"] for row in retrieval) / len(retrieval), 4)
            if retrieval
            else None,
            "citation_valid_cases": sum(
                row["checks"]["citation_membership"] and row["checks"]["citation_presence"]
                for row in rows
            ),
            "unsupported_abstention_checks": sum(
                row["checks"]["abstention"] for row in rows if row["expected_abstention"]
            ),
            "unsupported_cases": sum(row["expected_abstention"] for row in rows),
            "reliability_checks_passed": sum(
                row["checks"]["attempts"] and row["checks"]["error"]
                for row in rows
                if row["category"]
                in {"retryable_failure", "nonretryable_failure", "dependency_failure"}
            ),
            "unauthorized_writes_blocked": sum(
                write["state"] == "rejected"
                for row in rows
                if row["category"] in {"unapproved_write", "duplicate_write"}
                for write in row["writes"]
            ),
            "workflow_checks_passed": sum(
                row["checks"]["systems"] and row["checks"]["state"] for row in rows
            ),
            "failures": [row["name"] for row in rows if not row["passed"]],
        },
        "cases": rows,
    }
