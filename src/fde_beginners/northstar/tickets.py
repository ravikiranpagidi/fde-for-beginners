import logging

from mcp import Client
from pydantic import ValidationError

from fde_beginners.common.logging import event
from fde_beginners.northstar.data import Customer
from fde_beginners.safe_tools.approval import ApprovalStore, TicketRequest
from fde_beginners.safe_tools.server import create_server

logger = logging.getLogger(__name__)


async def execute_ticket(
    data: dict,
    store: ApprovalStore,
    request: TicketRequest,
    token: str | None,
    *,
    fail: bool = False,
) -> dict:
    restricted = set()
    for key, value in data["customers"].items():
        try:
            customer = Customer.model_validate(value)
        except ValidationError:
            restricted.add(key)
            continue
        if customer.customer_id != key or customer.region != "US" or customer.audience == "unknown":
            restricted.add(key)
    server = create_server(
        store,
        fail_writes=fail,
        customers=data["customers"],
        orders=data["orders"],
        restricted=frozenset(restricted),
    )
    async with Client(server) as client:
        response = await client.call_tool(
            "create_support_ticket",
            {**request.model_dump(), "approval_token": token},
        )
    event(logger, "write_rejected" if response.is_error else "write_executed")
    return {
        "state": "rejected" if response.is_error else "executed",
        "result": None if response.is_error else response.structured_content,
    }
