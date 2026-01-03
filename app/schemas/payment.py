from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.payment import PaymentStatus


class PaymentCreate(BaseModel):
    order_id: int
    provider: str = Field(default="MOCK", min_length=1, max_length=50)


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    provider: str
    payment_ref: Optional[str] = None
    status: PaymentStatus
    paid_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}
