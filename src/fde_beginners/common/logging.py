"""Standard logging with explicit, redacted event fields."""

import json
import logging


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def event(logger: logging.Logger, name: str, **fields: object) -> None:
    # Callers pass operational metadata only, never payloads or approval tokens.
    logger.info(json.dumps({"event": name, **fields}, sort_keys=True))
