from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class FailureMode(StrEnum):
    normal = "normal"
    timeout = "timeout"
    rate_limit = "rate_limit"
    server_error = "server_error"
    malformed_response = "malformed_response"
    duplicate_request = "duplicate_request"


class Order(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    order_id: str
    customer_id: str
    status: str
    quantity: int = Field(gt=0)


class ReservationRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    order_id: str = Field(pattern=r"^O[0-9]{3}$")
    quantity: int = Field(gt=0, le=100)


class Reservation(ReservationRequest):
    reservation_id: str
