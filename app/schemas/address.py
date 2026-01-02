from __future__ import annotations

from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=100)
    district: str = Field(..., min_length=1, max_length=100)
    full_address: str = Field(..., min_length=1)
    postal_code: str = Field(..., min_length=1, max_length=20)


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    user_id: int

    model_config = {"from_attributes": True}
