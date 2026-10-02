"""No external network in tests. Loopback exists only for the API transport check."""

import socket

import pytest


@pytest.fixture(autouse=True)
def no_external_connections(monkeypatch):
    original = socket.socket.connect

    def connect(sock, address):
        if isinstance(address, tuple) and address[0] not in {"127.0.0.1", "::1", "localhost"}:
            raise AssertionError(f"External network forbidden in tests: {address[0]}")
        return original(sock, address)

    monkeypatch.setattr(socket.socket, "connect", connect)
