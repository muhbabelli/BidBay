from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models import Order, UserRole
from app.schemas import OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/me", response_model=list[OrderResponse])
def list_my_orders(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    return (
        db.query(Order)
        .filter(Order.buyer_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )


@router.get("/sales", response_model=list[OrderResponse])
def list_my_sales(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    if current_user.role == UserRole.BUYER:
        return []
    return (
        db.query(Order)
        .filter(Order.seller_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
