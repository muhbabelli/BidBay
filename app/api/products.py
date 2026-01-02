from __future__ import annotations

from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, RequireSeller
from app.core.database import get_db
from app.models import Product, ProductImage, ProductStatus, UserRole
from app.schemas import ProductCreate, ProductImageCreate, ProductImageResponse, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


def get_product_or_404(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


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


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    return get_product_or_404(db, product_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: RequireSeller,
):
    if product_in.auction_end_at <= datetime.utcnow():
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
    if current_user.role != UserRole.ADMIN and product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this product")

    if product_in.auction_end_at is not None and product_in.auction_end_at <= datetime.utcnow():
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
    if current_user.role != UserRole.ADMIN and product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this product")

    db.delete(product)
    db.commit()
    return None


@router.post("/{product_id}/images", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
def add_product_image(
    product_id: int,
    image_in: ProductImageCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: RequireSeller,
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
