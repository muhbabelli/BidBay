from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models import Bid, Favorite, Product, ProductImage, ProductStatus, User
from app.schemas import ProductCreate, ProductImageCreate, ProductImageResponse, ProductResponse, ProductUpdate, ProductWithDetailsResponse, SellerInfo

router = APIRouter(prefix="/products", tags=["Products"])


def get_product_or_404(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def enrich_product_with_details(db: Session, product: Product, current_user_id: int) -> dict:
    """Add seller info, highest bid, and favorite status to product"""
    # Get seller info
    seller = db.query(User).filter(User.id == product.seller_id).first()

    # Get highest bid
    highest_bid_result = db.query(func.max(Bid.amount)).filter(Bid.product_id == product.id).scalar()

    # Get bid count
    bid_count = db.query(func.count(Bid.id)).filter(Bid.product_id == product.id).scalar()

    # Check if favorited by current user
    is_favorited = db.query(Favorite).filter(
        Favorite.user_id == current_user_id,
        Favorite.product_id == product.id
    ).first() is not None

    return {
        **{c.name: getattr(product, c.name) for c in product.__table__.columns},
        "images": product.images,
        "seller": SellerInfo(
            id=seller.id,
            full_name=seller.full_name,
            phone_number=seller.phone_number
        ) if seller else None,
        "highest_bid": highest_bid_result,
        "bid_count": bid_count or 0,
        "is_favorited": is_favorited,
    }


@router.get("/", response_model=list[ProductResponse])
def list_products(
    db: Annotated[Session, Depends(get_db)],
    status_filter: Optional[ProductStatus] = Query(None, alias="status"),
    category_id: Optional[int] = None,
    seller_id: Optional[int] = None,
    q: Optional[str] = None,
):
    query = db.query(Product)
    if status_filter:
        query = query.filter(Product.status == status_filter)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if seller_id:
        query = query.filter(Product.seller_id == seller_id)
    if q:
        query = query.filter(Product.title.ilike(f"%{q}%"))
    return query.order_by(Product.created_at.desc()).all()


@router.get("/feed", response_model=list[ProductWithDetailsResponse])
def get_feed(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
    q: Optional[str] = None,
):
    """Get all products from other users (not current user's products)"""
    query = db.query(Product).filter(
        Product.seller_id != current_user.id,
        Product.status == ProductStatus.ACTIVE,
    )
    if q:
        query = query.filter(Product.title.ilike(f"%{q}%"))

    products = query.order_by(Product.created_at.desc()).all()
    return [enrich_product_with_details(db, p, current_user.id) for p in products]


@router.get("/my-products", response_model=list[ProductWithDetailsResponse])
def get_my_products(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    """Get current user's products"""
    products = db.query(Product).filter(
        Product.seller_id == current_user.id
    ).order_by(Product.created_at.desc()).all()

    return [enrich_product_with_details(db, p, current_user.id) for p in products]


@router.get("/favorites", response_model=list[ProductWithDetailsResponse])
def get_favorite_products(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    """Get products favorited by current user"""
    products = db.query(Product).join(
        Favorite, Favorite.product_id == Product.id
    ).filter(
        Favorite.user_id == current_user.id
    ).order_by(Product.created_at.desc()).all()

    return [enrich_product_with_details(db, p, current_user.id) for p in products]


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    return get_product_or_404(db, product_id)


@router.get("/{product_id}/details", response_model=ProductWithDetailsResponse)
def get_product_details(
    product_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    """Get product with full details including seller info and highest bid"""
    product = get_product_or_404(db, product_id)
    return enrich_product_with_details(db, product, current_user.id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    if product_in.auction_end_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Auction end must be in the future")

    product = Product(
        seller_id=current_user.id,
        category_id=product_in.category_id,
        title=product_in.title,
        description=product_in.description,
        starting_price=product_in.starting_price,
        min_increment=product_in.min_increment,
        auction_end_at=product_in.auction_end_at,
        status=ProductStatus.ACTIVE,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    product = get_product_or_404(db, product_id)
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this product")

    if product_in.auction_end_at is not None and product_in.auction_end_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Auction end must be in the future")

    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    product = get_product_or_404(db, product_id)
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this product")

    db.delete(product)
    db.commit()
    return None


@router.post("/{product_id}/images", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
def add_product_image(
    product_id: int,
    image_in: ProductImageCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    product = get_product_or_404(db, product_id)
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add images")

    image = ProductImage(
        product_id=product_id,
        image_url=image_in.image_url,
        position=image_in.position,
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image
