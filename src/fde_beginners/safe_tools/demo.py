"""A real stdio client; the human approval path is outside the MCP tool surface."""

import asyncio
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from mcp import Client
from mcp.client.stdio import StdioServerParameters

from fde_beginners.safe_tools.approval import ApprovalStore, TicketRequest


async def demo() -> None:
    with TemporaryDirectory(prefix="fde-mcp-") as directory:
        path = Path(directory) / "tickets.db"
        operator = ApprovalStore(path)
        parameters = StdioServerParameters(
            command=sys.executable,
            args=["-m", "fde_beginners.safe_tools.server", "--db", str(path)],
        )
        async with Client(parameters, read_timeout_seconds=10) as client:
            listing = await client.list_tools()
            print("Tools:", ", ".join(tool.name for tool in listing.tools))
            read = await client.call_tool("lookup_order", {"order_id": "O100"})
            print("Read without approval:", "allowed" if not read.is_error else "ERROR")
            request = TicketRequest(customer_id="C001", summary="Review damaged item evidence")
            arguments = request.model_dump()
            denied = await client.call_tool("create_support_ticket", arguments)
            print("Write without approval:", "rejected" if denied.is_error else "ERROR")
            print("Proposed ticket:", request.model_dump_json())
            if input("Type APPROVE to create this synthetic ticket: ").strip() != "APPROVE":
                print("Declined. No ticket created.")
                return
            token = operator.issue(request)
            allowed = await client.call_tool(
                "create_support_ticket", {**arguments, "approval_token": token}
            )
            print("Write with approval:", json.dumps(allowed.structured_content))
            repeated = await client.call_tool(
                "create_support_ticket", {**arguments, "approval_token": token}
            )
            print("Reused approval:", "rejected" if repeated.is_error else "ERROR")
            if read.is_error or not denied.is_error or allowed.is_error or not repeated.is_error:
                raise RuntimeError("Demo behavior did not match the safety contract")


def main() -> None:
    asyncio.run(demo())


if __name__ == "__main__":
    main()
