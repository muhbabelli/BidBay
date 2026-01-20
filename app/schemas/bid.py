from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.bid import BidStatus


class BidderInfo(BaseModel):
    id: int
    full_name: str
    phone_number: Optional[str] = None

    model_config = {"from_attributes": True}


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


class BidWithBidderResponse(BidResponse):
    """Bid with bidder details - for sellers viewing bids on their products"""
    bidder: Optional[BidderInfo] = None


class MyBidResponse(BidResponse):
    """Bid with product and seller info - for viewing my bids"""
    product_title: Optional[str] = None
    seller: Optional[BidderInfo] = None  # Reusing BidderInfo structure for seller
