from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models import Order, OrderStatus, Payment, PaymentStatus, Product, ProductStatus
from app.schemas import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment_in: PaymentCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    order = db.query(Order).filter(Order.id == payment_in.order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to pay for this order")
    if order.status != OrderStatus.AWAITING_PAYMENT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order is not awaiting payment")

    payment = Payment(
        order_id=order.id,
        provider=payment_in.provider,
        payment_ref=f"MOCK-{order.id}-{int(datetime.utcnow().timestamp())}",
        status=PaymentStatus.SUCCESS,
        paid_at=datetime.utcnow(),
    )
    order.status = OrderStatus.PAID

    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product:
        product.status = ProductStatus.SOLD

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
