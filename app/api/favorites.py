from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models import Favorite, Product, ProductStatus
from app.schemas import FavoriteCreate, FavoriteResponse

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.get("/", response_model=list[FavoriteResponse])
def list_favorites(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    return (
        db.query(Favorite)
        .join(Product, Product.id == Favorite.product_id)
        .filter(
            Favorite.user_id == current_user.id,
            Product.status != ProductStatus.EXPIRED,
        )
        .all()
    )


@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(
    favorite_in: FavoriteCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    product = db.query(Product).filter(Product.id == favorite_in.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    existing = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == current_user.id,
            Favorite.product_id == favorite_in.product_id,
        )
        .first()
    )
    if existing:
        return existing

    favorite = Favorite(user_id=current_user.id, product_id=favorite_in.product_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    product_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    favorite = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == current_user.id,
            Favorite.product_id == product_id,
        )
        .first()
    )
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
    return None
