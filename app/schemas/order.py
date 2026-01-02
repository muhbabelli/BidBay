from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models.order import OrderStatus


class OrderResponse(BaseModel):
    id: int
    product_id: int
    buyer_id: int
    seller_id: int
    bid_id: int
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime

    model_config = {"from_attributes": True}
