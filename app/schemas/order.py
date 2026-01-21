from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.models.order import OrderStatus


class SellerInfo(BaseModel):
    id: int
    full_name: str
    phone_number: Optional[str] = None

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    product_id: int
    buyer_id: int
    seller_id: int
    bid_id: int
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    product_title: Optional[str] = None
    seller: Optional[SellerInfo] = None

    model_config = {"from_attributes": True}
