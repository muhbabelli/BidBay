from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models import Bid, BidStatus, Order, OrderStatus, Product, ProductStatus, User
from app.schemas import BidCreate, BidResponse, BidWithBidderResponse, BidderInfo, MyBidResponse, OrderResponse

router = APIRouter(prefix="/bids", tags=["Bids"])


def get_bid_or_404(db: Session, bid_id: int) -> Bid:
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid not found")
    return bid


@router.post("/", response_model=BidResponse, status_code=status.HTTP_201_CREATED)
def place_bid(
    bid_in: BidCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    product = db.query(Product).filter(Product.id == bid_in.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.status != ProductStatus.ACTIVE or product.auction_end_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Auction is not active")
    if product.seller_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot bid on your own product")

    highest = (
        db.query(Bid)
        .filter(Bid.product_id == product.id)
        .order_by(desc(Bid.amount))
        .first()
    )
    min_required = product.starting_price if not highest else highest.amount + product.min_increment
    if bid_in.amount < min_required:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bid must be at least {min_required}",
        )

    bid = Bid(product_id=product.id, bidder_id=current_user.id, amount=bid_in.amount)
    db.add(bid)
    db.flush()

    if highest and highest.status == BidStatus.PENDING:
        highest.status = BidStatus.OUTBID

    db.commit()
    db.refresh(bid)
    return bid


@router.get("/me", response_model=list[MyBidResponse])
def list_my_bids(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    """Get all bids placed by the current user with product and seller info"""
    bids = (
        db.query(Bid)
        .filter(Bid.bidder_id == current_user.id)
        .order_by(Bid.created_at.desc())
        .all()
    )

    result = []
    for bid in bids:
        product = db.query(Product).filter(Product.id == bid.product_id).first()
        seller = db.query(User).filter(User.id == product.seller_id).first() if product else None

        # Only show seller phone if bid is accepted
        seller_info = None
        if seller:
            seller_info = BidderInfo(
                id=seller.id,
                full_name=seller.full_name,
                phone_number=seller.phone_number if bid.status == BidStatus.ACCEPTED else None
            )

        result.append(MyBidResponse(
            id=bid.id,
            product_id=bid.product_id,
            bidder_id=bid.bidder_id,
            amount=bid.amount,
            status=bid.status,
            created_at=bid.created_at,
            product_title=product.title if product else None,
            seller=seller_info,
        ))

    return result


@router.get("/product/{product_id}", response_model=list[BidWithBidderResponse])
def list_product_bids(
    product_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    """Get all bids on a product (only for the product owner)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view bids")

    bids = (
        db.query(Bid)
        .filter(Bid.product_id == product_id)
        .order_by(desc(Bid.amount))
        .all()
    )

    result = []
    for bid in bids:
        bidder = db.query(User).filter(User.id == bid.bidder_id).first()
        result.append(BidWithBidderResponse(
            id=bid.id,
            product_id=bid.product_id,
            bidder_id=bid.bidder_id,
            amount=bid.amount,
            status=bid.status,
            created_at=bid.created_at,
            bidder=BidderInfo(
                id=bidder.id,
                full_name=bidder.full_name,
                phone_number=bidder.phone_number
            ) if bidder else None,
        ))

    return result


@router.post("/{bid_id}/accept", response_model=OrderResponse)
def accept_bid(
    bid_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    bid = get_bid_or_404(db, bid_id)
    product = db.query(Product).filter(Product.id == bid.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to accept bids")
    if product.status != ProductStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is not active")

    existing_order = db.query(Order).filter(Order.bid_id == bid.id).first()
    if existing_order:
        return existing_order

    bid.status = BidStatus.ACCEPTED
    product.accepted_bid_id = bid.id
    product.status = ProductStatus.SOLD

    db.query(Bid).filter(
        Bid.product_id == product.id,
        Bid.id != bid.id,
        Bid.status == BidStatus.PENDING,
    ).update({Bid.status: BidStatus.REJECTED})

    order = Order(
        product_id=product.id,
        buyer_id=bid.bidder_id,
        seller_id=product.seller_id,
        bid_id=bid.id,
        total_amount=bid.amount,
        status=OrderStatus.AWAITING_PAYMENT,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.post("/{bid_id}/reject", response_model=BidResponse)
def reject_bid(
    bid_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    bid = get_bid_or_404(db, bid_id)
    product = db.query(Product).filter(Product.id == bid.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to reject bids")

    bid.status = BidStatus.REJECTED
    db.commit()
    db.refresh(bid)
    return bid
