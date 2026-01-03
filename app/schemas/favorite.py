from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class FavoriteCreate(BaseModel):
    product_id: int


class FavoriteResponse(BaseModel):
    user_id: int
    product_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
