from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models import Order, Product, User
from app.schemas import OrderResponse
from app.schemas.order import SellerInfo

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/me", response_model=list[OrderResponse])
def list_my_orders(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    orders_list = (
        db.query(Order)
        .filter(Order.buyer_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    result = []
    for order in orders_list:
        product = db.query(Product).filter(Product.id == order.product_id).first()
        seller = db.query(User).filter(User.id == order.seller_id).first()

        order_dict = {
            "id": order.id,
            "product_id": order.product_id,
            "buyer_id": order.buyer_id,
            "seller_id": order.seller_id,
            "bid_id": order.bid_id,
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at,
            "product_title": product.title if product else None,
            "seller": SellerInfo(
                id=seller.id,
                full_name=seller.full_name,
                phone_number=seller.phone_number
            ) if seller else None
        }
        result.append(order_dict)

    return result


@router.get("/sales", response_model=list[OrderResponse])
def list_my_sales(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    return (
        db.query(Order)
        .filter(Order.seller_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
