from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, exists, func, select
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models import Bid, Favorite, Product, ProductStatus, User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/trending-products")
def trending_products(
    db: Annotated[Session, Depends(get_db)],
    min_favorites: int = Query(2, ge=1),
):
    stmt = (
        select(
            Product.id,
            Product.title,
            func.count(Favorite.product_id).label("favorite_count"),
        )
        .join(Favorite, Favorite.product_id == Product.id)
        .group_by(Product.id)
        .having(func.count(Favorite.product_id) >= min_favorites)
        .order_by(desc("favorite_count"))
    )
    return [dict(row._mapping) for row in db.execute(stmt).all()]


@router.get("/seller-bid-stats")
def seller_bid_stats(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    stmt = (
        select(
            Product.id.label("product_id"),
            Product.title,
            func.count(Bid.id).label("bid_count"),
            func.max(Bid.amount).label("max_bid"),
            func.avg(Bid.amount).label("avg_bid"),
        )
        .join(Bid, Bid.product_id == Product.id)
        .where(Product.seller_id == current_user.id)
        .group_by(Product.id)
        .having(func.count(Bid.id) >= 1)
        .order_by(desc("bid_count"))
    )
    return [dict(row._mapping) for row in db.execute(stmt).all()]


@router.get("/outbid-bids")
def outbid_bids(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    max_bid_subq = (
        select(Bid.product_id, func.max(Bid.amount).label("max_amount"))
        .group_by(Bid.product_id)
        .subquery()
    )
    stmt = (
        select(
            Bid.id,
            Bid.product_id,
            Bid.amount,
            max_bid_subq.c.max_amount,
        )
        .join(max_bid_subq, Bid.product_id == max_bid_subq.c.product_id)
        .where(Bid.bidder_id == current_user.id, Bid.amount < max_bid_subq.c.max_amount)
        .order_by(desc(max_bid_subq.c.max_amount))
    )
    return [dict(row._mapping) for row in db.execute(stmt).all()]


@router.get("/active-without-bids")
def active_without_bids(
    db: Annotated[Session, Depends(get_db)],
):
    has_bids = exists(select(Bid.id).where(Bid.product_id == Product.id))
    stmt = (
        select(Product.id, Product.title, Product.auction_end_at)
        .where(Product.status == ProductStatus.ACTIVE, ~has_bids)
        .order_by(Product.auction_end_at.asc())
    )
    return [dict(row._mapping) for row in db.execute(stmt).all()]


@router.get("/top-bidders")
def top_bidders(
    db: Annotated[Session, Depends(get_db)],
    min_bids: int = Query(2, ge=1),
):
    stmt = (
        select(
            User.id.label("user_id"),
            User.email,
            func.count(Bid.id).label("bid_count"),
        )
        .join(Bid, Bid.bidder_id == User.id)
        .group_by(User.id)
        .having(func.count(Bid.id) >= min_bids)
        .order_by(desc("bid_count"))
    )
    return [dict(row._mapping) for row in db.execute(stmt).all()]
