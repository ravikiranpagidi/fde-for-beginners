"""Loopback-only training API. Failure controls are deliberately not production controls."""

import asyncio
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from fde_beginners.common.data import ORDERS
from fde_beginners.integration.models import FailureMode, Reservation, ReservationRequest


def create_app() -> FastAPI:
    app = FastAPI(title="Northstar synthetic upstream")
    app.state.reservations = {}
    app.state.lock = asyncio.Lock()

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    async def inject(mode: FailureMode, attempt: int, failures: int) -> JSONResponse | None:
        if attempt > failures:
            return None
        if mode == FailureMode.timeout:
            await asyncio.sleep(0.5)
        if mode == FailureMode.rate_limit:
            return JSONResponse({"error": "rate_limited"}, 429, headers={"Retry-After": "0.05"})
        if mode == FailureMode.server_error:
            return JSONResponse({"error": "unavailable"}, 500)
        if mode == FailureMode.malformed_response:
            return JSONResponse({"quantity": "not-an-integer"})
        return None

    @app.get("/orders/{order_id}", response_model=None)
    async def order(
        order_id: str,
        mode: FailureMode = FailureMode.normal,
        failures: int = 1,
        x_attempt: Annotated[int, Header(ge=1)] = 1,
    ) -> dict | JSONResponse:
        fault = await inject(mode, x_attempt, failures)
        if fault is not None:
            return fault
        if order_id not in ORDERS:
            raise HTTPException(404, "Order not found")
        return ORDERS[order_id]

    @app.post("/reservations", response_model=None)
    async def reserve(
        payload: ReservationRequest,
        idempotency_key: Annotated[str, Header(min_length=1, max_length=100)],
        mode: FailureMode = FailureMode.normal,
        failures: int = 1,
        x_attempt: Annotated[int, Header(ge=1)] = 1,
    ) -> dict | JSONResponse:
        if payload.order_id not in ORDERS:
            raise HTTPException(404, "Order not found")
        fault = await inject(mode, x_attempt, failures)
        if fault is not None:
            return fault
        async with app.state.lock:
            previous = app.state.reservations.get(idempotency_key)
            if previous:
                if previous[0] != payload:
                    raise HTTPException(409, "Idempotency key used for different payload")
                result = previous[1]
            else:
                result = Reservation(
                    **payload.model_dump(), reservation_id=f"R{len(app.state.reservations) + 1:03}"
                ).model_dump()
                app.state.reservations[idempotency_key] = (payload, result)
        # The side effect already happened. A retry must recover the same result.
        if mode == FailureMode.duplicate_request and x_attempt <= failures:
            return JSONResponse({"error": "response_lost_after_commit"}, 503)
        return result

    return app


app = create_app()
