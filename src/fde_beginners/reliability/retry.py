import math
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime

RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


@dataclass(frozen=True)
class RetryPolicy:
    attempts: int = 3
    base_delay: float = 0.05
    max_delay: float = 1.0
    timeout: float = 0.15

    def __post_init__(self) -> None:
        if self.attempts < 1 or not all(
            math.isfinite(value) and value > 0
            for value in (self.base_delay, self.max_delay, self.timeout)
        ):
            raise ValueError("Retry attempts and finite timing values must be positive")

    def delay(self, attempt: int, retry_after: str | None = None) -> float | None:
        """Honor Retry-After or stop if waiting would exceed our local budget."""
        backoff = min(self.base_delay * 2 ** (attempt - 1), self.max_delay)
        if retry_after is None:
            return backoff
        try:
            seconds = float(retry_after)
        except ValueError:
            try:
                seconds = (parsedate_to_datetime(retry_after) - datetime.now(UTC)).total_seconds()
            except (ValueError, TypeError, OverflowError):
                return backoff
        if not math.isfinite(seconds) or seconds > self.max_delay:
            return None
        return max(backoff, seconds, 0)
