from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.product import ProductStatus
from app.schemas.product_image import ProductImageResponse


class SellerInfo(BaseModel):
    id: int
    full_name: str
    phone_number: Optional[str] = None

    model_config = {"from_attributes": True}


class ProductBase(BaseModel):
    category_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    starting_price: Decimal = Field(..., gt=0)
    min_increment: Decimal = Field(Decimal("1.00"), gt=0)
    auction_end_at: datetime


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    starting_price: Optional[Decimal] = Field(None, gt=0)
    min_increment: Optional[Decimal] = Field(None, gt=0)
    auction_end_at: Optional[datetime] = None
    status: Optional[ProductStatus] = None


class ProductResponse(ProductBase):
    id: int
    seller_id: int
    status: ProductStatus
    accepted_bid_id: Optional[int] = None
    created_at: datetime
    images: list[ProductImageResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class ProductWithDetailsResponse(ProductResponse):
    """Product with seller info and highest bid"""
    seller: Optional[SellerInfo] = None
    highest_bid: Optional[Decimal] = None
    bid_count: int = 0
    is_favorited: bool = False
