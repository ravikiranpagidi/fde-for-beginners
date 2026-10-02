import argparse
import json

import httpx

from fde_beginners.common.logging import configure_logging
from fde_beginners.integration.client import OrderClient
from fde_beginners.integration.models import FailureMode, ReservationRequest
from fde_beginners.reliability.errors import IntegrationError


def main() -> None:
    parser = argparse.ArgumentParser(description="Northstar reliable local API client")
    parser.add_argument("--url", default="http://127.0.0.1:8001")
    parser.add_argument("--mode", choices=list(FailureMode), default="normal")
    parser.add_argument("--failures", type=int, default=1)
    parser.add_argument("--reserve", action="store_true")
    parser.add_argument("--key", default="reservation-demo-1")
    args = parser.parse_args()
    configure_logging()
    try:
        with httpx.Client(base_url=args.url, trust_env=False) as http:
            client = OrderClient(http)
            fault = {"mode": args.mode, "failures": args.failures}
            if args.reserve:
                result = client.reserve(
                    ReservationRequest(order_id="O100", quantity=1), args.key, **fault
                )
            else:
                result = client.lookup(**fault)
            print(result.model_dump_json())
    except IntegrationError as exc:
        print(json.dumps({"status": "degraded", "code": exc.code, "attempts": exc.attempts}))
        raise SystemExit(2) from exc
