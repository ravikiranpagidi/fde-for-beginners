import argparse
import asyncio
import json
from pathlib import Path
from typing import get_args

from fde_beginners.common.logging import configure_logging
from fde_beginners.northstar.data import load_data
from fde_beginners.northstar.evaluation import evaluate
from fde_beginners.northstar.runtime import local_orders
from fde_beginners.northstar.tickets import execute_ticket
from fde_beginners.northstar.workflow import AssistRequest, Fault, SupportWorkflow, prepare_ticket
from fde_beginners.safe_tools.approval import ApprovalStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Northstar local synthetic support workflow")
    parser.add_argument("command", choices=["assist", "ticket", "evaluate"])
    parser.add_argument("--customer", default="C001")
    parser.add_argument("--order", default="O100")
    parser.add_argument("--question", default="What is the return window with a receipt?")
    parser.add_argument("--fault", choices=get_args(Fault), default="normal")
    parser.add_argument("--action-id", help="Keep stable on retries; defaults to review-ORDER_ID")
    parser.add_argument("--db", type=Path, default=Path(".fde-lab/northstar.db"))
    parser.add_argument("--report", type=Path, default=Path(".fde-lab/northstar-evaluation.json"))
    parser.add_argument("--without-approval", action="store_true")
    parser.add_argument("--ticket-failure", action="store_true")
    args = parser.parse_args()
    configure_logging()
    if args.command == "evaluate":
        report = asyncio.run(evaluate())
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report["summary"], indent=2))
        raise SystemExit(bool(report["summary"]["failures"]))
    data = load_data()
    with local_orders(data) as orders:
        result = SupportWorkflow(data, orders).assist(
            AssistRequest(
                customer_id=args.customer,
                order_id=args.order,
                question=args.question,
                fault=args.fault,
            )
        )
    print(result.model_dump_json(indent=2))
    if args.command == "ticket":
        if result.state != "drafted":
            print("No ticket prepared: resolve the evidence or access limitation first.")
            raise SystemExit(1)
        request = prepare_ticket(result, args.action_id or f"review-{args.order}")
        print("Exact mutation: CREATE support ticket " + request.model_dump_json())
        store, token = ApprovalStore(args.db), None
        if not args.without_approval:
            if (
                input("Review the exact payload. Type APPROVE to create this synthetic ticket: ")
                != "APPROVE"
            ):
                print("Cancelled; no approval issued and no write attempted.")
                return
            token = store.issue(request)
        outcome = asyncio.run(execute_ticket(data, store, request, token, fail=args.ticket_failure))
        print(json.dumps(outcome, indent=2))
        raise SystemExit(outcome["state"] == "rejected")


if __name__ == "__main__":
    main()
