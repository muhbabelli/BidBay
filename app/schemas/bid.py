from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.bid import BidStatus


class BidBase(BaseModel):
    product_id: int
    amount: Decimal = Field(..., gt=0)


class BidCreate(BidBase):
    pass


class BidResponse(BidBase):
    id: int
    bidder_id: int
    status: BidStatus
    created_at: datetime

    model_config = {"from_attributes": True}
