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
from app.models import (
    User,
    UserRole,
    Category,
    Product,
    ProductStatus,
    Bid,
    BidStatus,
    Order,
    OrderStatus,
    Payment,
    PaymentStatus,
)


def print_step(message: str) -> None:
    print(f"[STEP] {message}")


def main() -> None:
    db = SessionLocal()
    created = {
        "payment_id": None,
        "order_id": None,
        "bid_id": None,
        "bid2_id": None,
        "product_id": None,
        "category_id": None,
        "seller_id": None,
        "buyer_id": None,
        "buyer2_id": None,
    }
    try:
        print_step("Create seller and buyer users")
        seller = User(
            email="flow_seller@bidbay.com",
            password_hash=get_password_hash("password123"),
            full_name="Flow Seller",
            phone_number="+1-555-9991",
            role=UserRole.SELLER,
        )
        buyer = User(
            email="flow_buyer@bidbay.com",
            password_hash=get_password_hash("password123"),
            full_name="Flow Buyer",
            phone_number="+1-555-9992",
            role=UserRole.BUYER,
        )
        buyer_two = User(
            email="flow_buyer2@bidbay.com",
            password_hash=get_password_hash("password123"),
            full_name="Flow Buyer Two",
            phone_number="+1-555-9993",
            role=UserRole.BUYER,
        )
        db.add_all([seller, buyer, buyer_two])
        db.commit()
        db.refresh(seller)
        db.refresh(buyer)
        db.refresh(buyer_two)
        created["seller_id"] = seller.id
        created["buyer_id"] = buyer.id
        created["buyer2_id"] = buyer_two.id
        print(f"[INFO] Seller created: id={seller.id}, email={seller.email}, role={seller.role}")
        print(f"[INFO] Buyer created: id={buyer.id}, email={buyer.email}, role={buyer.role}")
        print(f"[INFO] Buyer2 created: id={buyer_two.id}, email={buyer_two.email}, role={buyer_two.role}")

        print_step("Create a category")
        category = Category(name=f"Flow Category {int(datetime.utcnow().timestamp())}")
        db.add(category)
        db.commit()
        db.refresh(category)
        created["category_id"] = category.id
        print(f"[INFO] Category created: id={category.id}, name={category.name}")

        print_step("Create a product listing")
        product = Product(
            seller_id=seller.id,
            category_id=category.id,
            title="Flow Test Product",
            description="Flow test description",
            starting_price=Decimal("100.00"),
            min_increment=Decimal("10.00"),
            auction_end_at=datetime.utcnow() + timedelta(days=1),
            status=ProductStatus.ACTIVE,
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        created["product_id"] = product.id
        print(
            "[INFO] Product created: "
            f"id={product.id}, title={product.title}, start={product.starting_price}, "
            f"min_inc={product.min_increment}, status={product.status}"
        )

        print_step("Place a valid bid")
        bid = Bid(
            product_id=product.id,
            bidder_id=buyer.id,
            amount=Decimal("110.00"),
            status=BidStatus.PENDING,
        )
        db.add(bid)
        db.commit()
        db.refresh(bid)
        created["bid_id"] = bid.id
        assert bid.amount >= product.starting_price
        print(
            "[INFO] Bid placed: "
            f"id={bid.id}, bidder_id={buyer.id}, bidder_email={buyer.email}, "
            f"product_id={bid.product_id}, amount={bid.amount}, status={bid.status}"
        )

        print_step("Place a second bid from another buyer")
        bid_two = Bid(
            product_id=product.id,
            bidder_id=buyer_two.id,
            amount=Decimal("125.00"),
            status=BidStatus.PENDING,
        )
        db.add(bid_two)
        db.commit()
        db.refresh(bid_two)
        created["bid2_id"] = bid_two.id
        assert bid_two.amount > bid.amount
        print(
            "[INFO] Bid placed: "
            f"id={bid_two.id}, bidder_id={buyer_two.id}, bidder_email={buyer_two.email}, "
            f"product_id={bid_two.product_id}, amount={bid_two.amount}, status={bid_two.status}"
        )

        print_step("Accept the bid and create an order")
        bid_two.status = BidStatus.ACCEPTED
        bid.status = BidStatus.OUTBID
        product.accepted_bid_id = bid_two.id
        product.status = ProductStatus.CLOSED
        order = Order(
            product_id=product.id,
            buyer_id=buyer_two.id,
            seller_id=seller.id,
            bid_id=bid_two.id,
            total_amount=bid_two.amount,
            status=OrderStatus.AWAITING_PAYMENT,
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        created["order_id"] = order.id
        print(
            "[INFO] Order created: "
            f"id={order.id}, bid_id={order.bid_id}, buyer_id={order.buyer_id}, "
            f"seller_id={order.seller_id}, total={order.total_amount}, status={order.status}"
        )

        print_step("Record a mock payment and mark order/product as complete")
        payment = Payment(
            order_id=order.id,
            provider="MOCK",
            payment_ref=f"FLOW-{order.id}",
            status=PaymentStatus.SUCCESS,
            paid_at=datetime.utcnow(),
        )
        order.status = OrderStatus.PAID
        product.status = ProductStatus.SOLD
        db.add(payment)
        db.commit()
        db.refresh(payment)
        created["payment_id"] = payment.id
        print(
            "[INFO] Payment recorded: "
            f"id={payment.id}, order_id={payment.order_id}, status={payment.status}, ref={payment.payment_ref}"
        )
        print(f"[INFO] Product status updated: id={product.id}, status={product.status}")
        print(f"[INFO] Order status updated: id={order.id}, status={order.status}")

        print_step("Verify final states")
        assert product.status == ProductStatus.SOLD
        assert order.status == OrderStatus.PAID
        assert payment.status == PaymentStatus.SUCCESS

        print_step("Flow test completed successfully")
    finally:
        print_step("Cleaning up flow test data")
        if created.get("product_id"):
            db.query(Product).filter(Product.id == created["product_id"]).update(
                {Product.accepted_bid_id: None}
            )
            db.commit()
        for model, key in [
            (Payment, "payment_id"),
            (Order, "order_id"),
            (Bid, "bid2_id"),
            (Bid, "bid_id"),
            (Product, "product_id"),
            (Category, "category_id"),
            (User, "seller_id"),
            (User, "buyer2_id"),
            (User, "buyer_id"),
        ]:
            record_id = created.get(key)
            if record_id:
                db.query(model).filter(model.id == record_id).delete()
                print(f"[INFO] Deleted {model.__name__} id={record_id}")
        db.commit()
        db.close()


if __name__ == "__main__":
    main()
