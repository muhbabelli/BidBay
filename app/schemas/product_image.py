from __future__ import annotations

from pydantic import BaseModel, Field


class ProductImageBase(BaseModel):
    image_url: str = Field(..., min_length=1, max_length=500)
    position: int = Field(0, ge=0)


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageResponse(ProductImageBase):
    id: int
    product_id: int

    model_config = {"from_attributes": True}
