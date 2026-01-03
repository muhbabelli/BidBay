from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.database import SessionLocal
from app.models import User, Product, Bid, Order, Payment, Category


FLOW_EMAILS = ["flow_seller@bidbay.com", "flow_buyer@bidbay.com"]
FLOW_PRODUCT_TITLE = "Flow Test Product"


def print_step(message: str) -> None:
    print(f"[STEP] {message}")


def main() -> None:
    db = SessionLocal()
    try:
        print_step("Locate flow users")
        users = db.query(User).filter(User.email.in_(FLOW_EMAILS)).all()
        user_ids = [u.id for u in users]

        print_step("Locate bids created by flow users")
        bids = db.query(Bid).filter(Bid.bidder_id.in_(user_ids)).all() if user_ids else []
        bid_ids = [b.id for b in bids]

        print_step("Clear accepted_bid_id references")
        if bid_ids:
            db.query(Product).filter(Product.accepted_bid_id.in_(bid_ids)).update(
                {Product.accepted_bid_id: None}, synchronize_session=False
            )
        db.query(Product).filter(Product.title == FLOW_PRODUCT_TITLE).update(
            {Product.accepted_bid_id: None}, synchronize_session=False
        )
        db.commit()

        print_step("Delete payments and orders")
        if user_ids:
            orders = db.query(Order).filter(Order.buyer_id.in_(user_ids)).all()
            order_ids = [o.id for o in orders]
        else:
            order_ids = []
        if order_ids:
            db.query(Payment).filter(Payment.order_id.in_(order_ids)).delete(synchronize_session=False)
            db.query(Order).filter(Order.id.in_(order_ids)).delete(synchronize_session=False)

        print_step("Delete bids")
        if bid_ids:
            db.query(Bid).filter(Bid.id.in_(bid_ids)).delete(synchronize_session=False)

        print_step("Delete flow product and categories")
        db.query(Product).filter(Product.title == FLOW_PRODUCT_TITLE).delete(synchronize_session=False)
        db.query(Category).filter(Category.name.like("Flow Category%")).delete(synchronize_session=False)

        print_step("Delete flow users")
        if user_ids:
            db.query(User).filter(User.id.in_(user_ids)).delete(synchronize_session=False)

        db.commit()
        print_step("Cleanup completed")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
