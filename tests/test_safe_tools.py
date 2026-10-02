import asyncio
import logging
import sys
from concurrent.futures import ThreadPoolExecutor

import pytest
from mcp import Client
from mcp.client.stdio import StdioServerParameters

from fde_beginners.safe_tools.approval import ApprovalRequired, ApprovalStore, TicketRequest
from fde_beginners.safe_tools.server import create_server


@pytest.fixture
def store(tmp_path):
    return ApprovalStore(tmp_path / "tickets.db")


def request():
    return TicketRequest(customer_id="C001", summary="Review damaged item evidence")


def test_approval_is_action_bound_expiring_and_one_time(store):
    token = store.issue(request())
    with pytest.raises(ApprovalRequired):
        store.execute(TicketRequest(customer_id="C001", summary="Different action"), token)
    assert store.execute(request(), token)["status"] == "created"
    with pytest.raises(ApprovalRequired):
        store.execute(request(), token)
    expired = store.issue(request(), lifetime=-1)
    with pytest.raises(ApprovalRequired):
        store.execute(request(), expired)
    assert store.ticket_count() == 1


def test_competing_writes_consume_one_approval_once(store):
    token = store.issue(request())

    def execute():
        try:
            store.execute(request(), token)
            return "created"
        except ApprovalRequired:
            return "denied"

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(lambda _: execute(), range(2)))
    assert sorted(outcomes) == ["created", "denied"]
    assert store.ticket_count() == 1


def test_tools_over_real_mcp_protocol_in_process(store, caplog):
    caplog.set_level(logging.INFO)

    async def scenario():
        async with Client(create_server(store)) as client:
            tools = (await client.list_tools()).tools
            assert {t.name for t in tools} == {
                "search_customer",
                "lookup_order",
                "search_policy",
                "create_support_ticket",
            }
            for name, args in [
                ("search_customer", {"query": "C001"}),
                ("lookup_order", {"order_id": "O100"}),
                ("search_policy", {"query": "return window"}),
            ]:
                assert not (await client.call_tool(name, args)).is_error
            for args in [
                request().model_dump(),
                {**request().model_dump(), "approval_token": "invalid"},
            ]:
                assert (await client.call_tool("create_support_ticket", args)).is_error
            token = store.issue(request())
            args = {**request().model_dump(), "approval_token": token}
            result = await client.call_tool("create_support_ticket", args)
            assert not result.is_error
            assert result.structured_content["status"] == "created"
            assert (await client.call_tool("create_support_ticket", args)).is_error
            assert store.ticket_count() == 1

    asyncio.run(scenario())
    audit = [r.message for r in caplog.records if '"event": "tool_audit"' in r.message]
    assert any(
        '"operation_type": "WRITE"' in text and '"result": "ApprovalRequired"' in text
        for text in audit
    )
    assert any('"approval_status": "valid_consumed"' in text for text in audit)
    assert all("Review damaged" not in text and "approval_token" not in text for text in audit)


@pytest.mark.parametrize(
    "tool,args",
    [
        ("lookup_order", {"order_id": "O999"}),
        ("search_customer", {"query": "Nobody"}),
        ("search_customer", {"query": ""}),
        ("create_support_ticket", {"customer_id": "C001", "summary": "x"}),
        ("create_support_ticket", {"customer_id": "bad", "summary": "Valid summary"}),
        ("create_support_ticket", {"customer_id": "C999", "summary": "Valid summary"}),
        ("lookup_order", {"wrong_parameter": 42}),
    ],
)
def test_missing_resources_and_invalid_inputs_fail_safely(store, tool, args):
    async def scenario():
        async with Client(create_server(store)) as client:
            result = await client.call_tool(tool, args)
            assert result.is_error
            assert store.ticket_count() == 0

    asyncio.run(scenario())


def test_downstream_failure_does_not_consume_approval_or_create_ticket(store):
    token = store.issue(request())

    async def scenario():
        async with Client(create_server(store, fail_writes=True)) as client:
            result = await client.call_tool(
                "create_support_ticket", {**request().model_dump(), "approval_token": token}
            )
            assert result.is_error
            assert store.ticket_count() == 0

    asyncio.run(scenario())
    assert store.execute(request(), token)["status"] == "created"


def test_stdio_server_round_trip_including_approved_write(store):
    async def scenario():
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "fde_beginners.safe_tools.server", "--db", str(store.path)],
        )
        async with Client(params, read_timeout_seconds=10) as client:
            assert not (await client.call_tool("lookup_order", {"order_id": "O100"})).is_error
            assert (
                await client.call_tool("create_support_ticket", request().model_dump())
            ).is_error
            token = store.issue(request())
            result = await client.call_tool(
                "create_support_ticket", {**request().model_dump(), "approval_token": token}
            )
            assert not result.is_error
            assert result.structured_content["ticket_id"] == "T001"

    asyncio.run(scenario())
    assert store.ticket_count() == 1


def test_storage_error_is_reported_as_failure_in_audit(store, caplog):
    caplog.set_level(logging.INFO)
    token = store.issue(request())
    with store.connect() as connection:
        connection.execute("DROP TABLE tickets")

    async def scenario():
        async with Client(create_server(store)) as client:
            result = await client.call_tool(
                "create_support_ticket", {**request().model_dump(), "approval_token": token}
            )
            assert result.is_error

    asyncio.run(scenario())
    audits = [r.message for r in caplog.records if '"event": "tool_audit"' in r.message]
    assert len(audits) == 1
    assert '"result": "DownstreamFailure"' in audits[0]
    assert token not in audits[0]
