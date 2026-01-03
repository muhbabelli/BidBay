from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models import Category, Favorite, Product, ProductStatus, User, UserRole


def print_step(message: str) -> None:
    print(f"[STEP] {message}")


def main() -> None:
    db = SessionLocal()
    created = {
        "favorite_id": None,
        "product_id": None,
        "category_id": None,
        "buyer_id": None,
        "seller_id": None,
    }
    suffix = int(datetime.utcnow().timestamp())
    try:
        print_step("Create seller and buyer for favorites flow")
        seller = User(
            email=f"fav_seller_{suffix}@bidbay.com",
            password_hash=get_password_hash("password123"),
            full_name="Favorites Seller",
            phone_number="+1-555-7771",
            role=UserRole.SELLER,
        )
        buyer = User(
            email=f"fav_buyer_{suffix}@bidbay.com",
            password_hash=get_password_hash("password123"),
            full_name="Favorites Buyer",
            phone_number="+1-555-7772",
            role=UserRole.BUYER,
        )
        db.add_all([seller, buyer])
        db.commit()
        db.refresh(seller)
        db.refresh(buyer)
        created["seller_id"] = seller.id
        created["buyer_id"] = buyer.id
        print(f"[INFO] Seller created: id={seller.id}, email={seller.email}")
        print(f"[INFO] Buyer created: id={buyer.id}, email={buyer.email}")

        print_step("Create category and product")
        category = Category(name=f"Favorites Category {suffix}")
        db.add(category)
        db.commit()
        db.refresh(category)
        created["category_id"] = category.id
        product = Product(
            seller_id=seller.id,
            category_id=category.id,
            title=f"Favorites Test Product {suffix}",
            description="Favorites flow test product",
            starting_price=Decimal("50.00"),
            min_increment=Decimal("5.00"),
            auction_end_at=datetime.utcnow() + timedelta(days=1),
            status=ProductStatus.ACTIVE,
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        created["product_id"] = product.id
        print(f"[INFO] Product created: id={product.id}, title={product.title}")

        print_step("Add product to favorites")
        favorite = Favorite(user_id=buyer.id, product_id=product.id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        created["favorite_id"] = favorite.product_id
        print(f"[INFO] Favorite created: user_id={favorite.user_id}, product_id={favorite.product_id}")

        print_step("Verify favorite exists")
        exists = (
            db.query(Favorite)
            .filter(Favorite.user_id == buyer.id, Favorite.product_id == product.id)
            .first()
        )
        assert exists is not None

        print_step("Remove favorite")
        db.query(Favorite).filter(
            Favorite.user_id == buyer.id,
            Favorite.product_id == product.id,
        ).delete()
        db.commit()
        print(f"[INFO] Favorite removed: user_id={buyer.id}, product_id={product.id}")

        print_step("Verify favorite removed")
        exists = (
            db.query(Favorite)
            .filter(Favorite.user_id == buyer.id, Favorite.product_id == product.id)
            .first()
        )
        assert exists is None

        print_step("Favorites test completed successfully")
    finally:
        print_step("Cleaning up favorites test data")
        db.query(Favorite).filter(
            Favorite.user_id == created.get("buyer_id"),
            Favorite.product_id == created.get("product_id"),
        ).delete()
        if created.get("product_id"):
            db.query(Product).filter(Product.id == created["product_id"]).delete()
        if created.get("category_id"):
            db.query(Category).filter(Category.id == created["category_id"]).delete()
        if created.get("buyer_id"):
            db.query(User).filter(User.id == created["buyer_id"]).delete()
        if created.get("seller_id"):
            db.query(User).filter(User.id == created["seller_id"]).delete()
        db.commit()
        db.close()


if __name__ == "__main__":
    main()
