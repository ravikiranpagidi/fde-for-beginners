import logging
import time
from collections.abc import Callable
from typing import TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from fde_beginners.common.logging import event
from fde_beginners.integration.models import Order, Reservation, ReservationRequest
from fde_beginners.reliability.errors import UpstreamUnavailable, ValidationFailure
from fde_beginners.reliability.retry import RETRYABLE_STATUS, RetryPolicy

logger = logging.getLogger(__name__)
ResponseT = TypeVar("ResponseT", bound=BaseModel)


class OrderClient:
    def __init__(
        self,
        http: httpx.Client,
        policy: RetryPolicy | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.http, self.policy, self.sleep = http, policy or RetryPolicy(), sleep

    def _request(
        self,
        method: str,
        path: str,
        schema: type[ResponseT],
        *,
        params: dict | None = None,
        payload: dict | None = None,
        key: str | None = None,
    ) -> ResponseT:
        for attempt in range(1, self.policy.attempts + 1):
            headers = {"X-Attempt": str(attempt)}
            if key is not None:
                headers["Idempotency-Key"] = key
            retry_after = None
            try:
                response = self.http.request(
                    method,
                    path,
                    json=payload,
                    params=params,
                    headers=headers,
                    timeout=self.policy.timeout,
                )
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                code = "timeout" if isinstance(exc, httpx.TimeoutException) else "network_error"
            else:
                if response.status_code in RETRYABLE_STATUS:
                    code = f"http_{response.status_code}"
                    retry_after = response.headers.get("Retry-After")
                elif response.status_code >= 300:
                    raise ValidationFailure(
                        f"http_{response.status_code}", attempt, "Non-retryable upstream response"
                    )
                else:
                    try:
                        result = schema.model_validate(response.json())
                    except (ValidationError, ValueError) as exc:
                        raise ValidationFailure(
                            "invalid_response", attempt, "Upstream response failed validation"
                        ) from exc
                    event(logger, "upstream_success", attempts=attempt, operation=method)
                    return result
            delay = self.policy.delay(attempt, retry_after)
            if attempt == self.policy.attempts or delay is None:
                raise UpstreamUnavailable(
                    code, attempt, "Use the manual workflow; upstream unavailable"
                )
            event(logger, "request_retry_scheduled", attempt=attempt, code=code, delay=delay)
            self.sleep(delay)
        raise AssertionError("unreachable")

    def lookup(self, order_id: str = "O100", **failure: object) -> Order:
        return self._request("GET", f"/orders/{order_id}", Order, params=failure)

    def reserve(self, payload: ReservationRequest, key: str, **failure: object) -> Reservation:
        if not key.strip() or len(key) > 100:
            raise ValidationFailure("invalid_key", 0, "A nonempty idempotency key is required")
        return self._request(
            "POST",
            "/reservations",
            Reservation,
            params=failure,
            payload=payload.model_dump(),
            key=key,
        )
