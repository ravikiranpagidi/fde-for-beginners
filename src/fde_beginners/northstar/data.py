import json
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PROJECT = Path("project/northstar-support-copilot")


class Customer(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    customer_id: str = Field(pattern=r"^C[0-9]{3}$")
    name: str = Field(min_length=1)
    audience: Literal["retail", "business", "unknown"]
    region: Literal["US", "EU"]


class OrderDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    placed_at: date
    delivered_at: date | None
    condition: Literal["opened", "unopened"]


def load_data() -> dict:
    """Keep deliberately malformed rows raw until the workflow boundary validates them."""
    return json.loads((PROJECT / "data.json").read_text(encoding="utf-8"))
