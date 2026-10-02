"""Trusted local operator store. Never expose issue() as an MCP tool."""

import hashlib
import secrets
import sqlite3
import time
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class TicketRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", str_strip_whitespace=True)
    customer_id: str = Field(pattern=r"^C[0-9]{3}$")
    summary: str = Field(min_length=5, max_length=200)


class ApprovalRequired(ValueError):
    pass


class DownstreamFailure(RuntimeError):
    pass


class ApprovalStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS approvals (
                    digest TEXT PRIMARY KEY, payload TEXT NOT NULL,
                    expires REAL NOT NULL, used INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY, payload TEXT NOT NULL
                );
            """)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        with closing(sqlite3.connect(self.path, timeout=5)) as connection:
            with connection:
                yield connection

    def issue(self, request: TicketRequest, *, lifetime: float = 300) -> str:
        """Called only after the trusted operator explicitly approves this payload."""
        token = secrets.token_urlsafe(32)
        digest = hashlib.sha256(token.encode()).hexdigest()
        with self.connect() as connection:
            connection.execute(
                "INSERT INTO approvals(digest, payload, expires) VALUES (?, ?, ?)",
                (digest, request.model_dump_json(), time.time() + lifetime),
            )
        return token

    def execute(self, request: TicketRequest, token: str | None, *, fail: bool = False) -> dict:
        if not token:
            raise ApprovalRequired("Explicit approval required")
        digest = hashlib.sha256(token.encode()).hexdigest()
        with self.connect() as connection:
            # Atomic consume and effect in one local transaction, including competing callers.
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT payload, expires, used FROM approvals WHERE digest = ?", (digest,)
            ).fetchone()
            if not row or row[0] != request.model_dump_json() or row[1] <= time.time() or row[2]:
                raise ApprovalRequired("Approval invalid, expired, consumed, or for another action")
            if fail:
                raise DownstreamFailure("Ticket store unavailable; no effect committed")
            cursor = connection.execute("INSERT INTO tickets(payload) VALUES (?)", (row[0],))
            connection.execute("UPDATE approvals SET used = 1 WHERE digest = ?", (digest,))
            return {"ticket_id": f"T{cursor.lastrowid:03}", "status": "created"}

    def ticket_count(self) -> int:
        with self.connect() as connection:
            return connection.execute("SELECT count(*) FROM tickets").fetchone()[0]
