import socket
import threading
import time

import httpx
import pytest
import uvicorn
from fastapi.testclient import TestClient

from fde_beginners.integration.client import OrderClient
from fde_beginners.integration.models import ReservationRequest
from fde_beginners.integration.upstream import create_app
from fde_beginners.reliability.errors import UpstreamUnavailable, ValidationFailure
from fde_beginners.reliability.retry import RetryPolicy


@pytest.fixture
def upstream():
    app = create_app()
    with TestClient(app) as http:
        yield app, http


def test_normal_read(upstream):
    _, http = upstream
    assert OrderClient(http).lookup().order_id == "O100"


@pytest.mark.parametrize("mode", ["rate_limit", "server_error"])
def test_transient_http_failure_retries_and_recovers(upstream, mode):
    _, http = upstream
    waits = []
    result = OrderClient(http, sleep=waits.append).lookup(mode=mode, failures=2)
    assert result.order_id == "O100"
    assert waits == [0.05, 0.1]


def test_retry_exhaustion_is_structured_and_bounded(upstream):
    _, http = upstream
    waits = []
    with pytest.raises(UpstreamUnavailable) as error:
        OrderClient(http, sleep=waits.append).lookup(mode="server_error", failures=10)
    assert error.value.attempts == 3
    assert error.value.code == "http_500"
    assert waits == [0.05, 0.1]


@pytest.mark.parametrize("mode", ["malformed_response"])
def test_invalid_upstream_schema_is_not_retried(upstream, mode):
    _, http = upstream
    waits = []
    with pytest.raises(ValidationFailure) as error:
        OrderClient(http, sleep=waits.append).lookup(mode=mode)
    assert error.value.code == "invalid_response"
    assert error.value.attempts == 1
    assert waits == []


def test_missing_order_is_not_retried(upstream):
    _, http = upstream
    with pytest.raises(ValidationFailure) as error:
        OrderClient(http).lookup("O999")
    assert error.value.code == "http_404"
    assert error.value.attempts == 1


def test_uncertain_write_and_repeated_request_have_one_effect(upstream):
    app, http = upstream
    client = OrderClient(http, sleep=lambda _: None)
    payload = ReservationRequest(order_id="O100", quantity=1)
    first = client.reserve(payload, "logical-request", mode="duplicate_request")
    repeated = client.reserve(payload, "logical-request")
    assert first == repeated
    assert len(app.state.reservations) == 1
    with pytest.raises(ValidationFailure) as error:
        client.reserve(ReservationRequest(order_id="O100", quantity=2), "logical-request")
    assert error.value.code == "http_409"
    assert len(app.state.reservations) == 1


def test_bad_request_and_missing_key_are_rejected_by_upstream(upstream):
    app, http = upstream
    assert http.post("/reservations", json={"order_id": "O100", "quantity": 0}).status_code == 422
    assert http.post("/reservations", json={"order_id": "O100", "quantity": 1}).status_code == 422
    assert not app.state.reservations


def test_timeout_exhaustion_without_slow_sleep():
    calls, waits = [], []

    def timeout(request):
        calls.append(request)
        raise httpx.ReadTimeout("controlled timeout", request=request)

    with httpx.Client(transport=httpx.MockTransport(timeout), base_url="http://test") as http:
        with pytest.raises(UpstreamUnavailable) as error:
            OrderClient(http, sleep=waits.append).lookup()
    assert error.value.code == "timeout"
    assert len(calls) == 3
    assert len(waits) == 2


def test_large_retry_after_does_not_retry_earlier_than_requested():
    waits = []

    def limited(request):
        return httpx.Response(429, headers={"Retry-After": "3600"})

    with httpx.Client(transport=httpx.MockTransport(limited), base_url="http://test") as http:
        with pytest.raises(UpstreamUnavailable) as error:
            OrderClient(http, sleep=waits.append).lookup()
    assert error.value.attempts == 1
    assert waits == []


@pytest.mark.parametrize("value", ["NaN", "inf"])
def test_invalid_unbounded_retry_after_stops(value):
    assert RetryPolicy().delay(1, value) is None


@pytest.fixture
def live_upstream():
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(create_app(), log_level="error"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    deadline = time.monotonic() + 5
    try:
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.started, "Local upstream did not start"
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        sock.close()
        assert not thread.is_alive(), "Local upstream did not stop"


def test_real_socket_timeout_recovers_on_next_attempt(live_upstream):
    waits = []
    with httpx.Client(base_url=live_upstream, trust_env=False) as http:
        result = OrderClient(http, sleep=waits.append).lookup(mode="timeout")
    assert result.order_id == "O100"
    assert waits == [0.05]
