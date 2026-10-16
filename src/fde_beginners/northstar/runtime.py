"""A real loopback HTTP dependency, including actual socket timeouts."""

import socket
import threading
import time
from contextlib import contextmanager

import httpx
import uvicorn

from fde_beginners.integration.client import OrderClient
from fde_beginners.integration.upstream import create_app


@contextmanager
def local_orders(data: dict):
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(create_app(data["orders"]), log_level="error"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 5
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        if not server.started:
            raise RuntimeError("Loopback order service did not start")
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", trust_env=False) as http:
            yield OrderClient(http)
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        sock.close()
        if thread.is_alive():
            raise RuntimeError("Loopback order service did not stop")
