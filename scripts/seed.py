"""
Database seeding script for BidBay.
Creates realistic sample data for testing and development.

Usage:
    cd BidBay
    conda run -n bidbay python -m scripts.seed
"""

import random
from datetime import datetime, timedelta
from decimal import Decimal

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models import (
    User, Address, Category, Product, ProductStatus,
    ProductImage, Bid, BidStatus, Favorite, Order, OrderStatus, Payment, PaymentStatus
)


# Sample data
CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home & Garden",
    "Sports & Outdoors",
    "Collectibles & Art",
    "Vehicles",
    "Toys & Hobbies",
    "Books & Media",
    "Jewelry & Watches",
    "Health & Beauty",
]

SAMPLE_USERS = [
    {"email": "user1@bidbay.com", "full_name": "John's Electronics", "phone": "+1-555-0101"},
    {"email": "user2@bidbay.com", "full_name": "Fashion House NYC", "phone": "+1-555-0102"},
    {"email": "user3@bidbay.com", "full_name": "Vintage Collectibles", "phone": "+1-555-0103"},
    {"email": "user4@bidbay.com", "full_name": "Sports Gear Pro", "phone": "+1-555-0104"},
    {"email": "user5@bidbay.com", "full_name": "Home Decor Plus", "phone": "+1-555-0105"},
    {"email": "user6@bidbay.com", "full_name": "Alice Johnson", "phone": "+1-555-0201"},
    {"email": "user7@bidbay.com", "full_name": "Bob Smith", "phone": "+1-555-0202"},
    {"email": "user8@bidbay.com", "full_name": "Carol Williams", "phone": "+1-555-0203"},
    {"email": "user9@bidbay.com", "full_name": "David Brown", "phone": "+1-555-0204"},
    {"email": "user10@bidbay.com", "full_name": "Emma Davis", "phone": "+1-555-0205"},
    {"email": "user11@bidbay.com", "full_name": "Frank Miller", "phone": "+1-555-0206"},
    {"email": "user12@bidbay.com", "full_name": "Grace Wilson", "phone": "+1-555-0207"},
    {"email": "user13@bidbay.com", "full_name": "Henry Taylor", "phone": "+1-555-0208"},
    {"email": "admin@bidbay.com", "full_name": "System Admin", "phone": "+1-555-0001"},
]

SAMPLE_PRODUCTS = [
    # Electronics
    {"title": "iPhone 15 Pro Max 256GB", "desc": "Brand new, sealed in box. Space Black color.", "price": 999.00, "increment": 25.00, "cat": "Electronics"},
    {"title": "MacBook Pro 14\" M3 Pro", "desc": "16GB RAM, 512GB SSD. AppleCare+ included.", "price": 1799.00, "increment": 50.00, "cat": "Electronics"},
    {"title": "Sony PlayStation 5", "desc": "Disc Edition with extra controller.", "price": 449.00, "increment": 15.00, "cat": "Electronics"},
    {"title": "Samsung 65\" OLED TV", "desc": "2024 model, perfect condition, wall mount included.", "price": 1299.00, "increment": 50.00, "cat": "Electronics"},
    {"title": "DJI Mavic 3 Pro Drone", "desc": "Fly More Combo with extra batteries.", "price": 1899.00, "increment": 50.00, "cat": "Electronics"},
    {"title": "Canon EOS R5 Camera Body", "desc": "Low shutter count, excellent condition.", "price": 2499.00, "increment": 75.00, "cat": "Electronics"},
    {"title": "Apple Watch Ultra 2", "desc": "With Alpine Loop band, barely used.", "price": 699.00, "increment": 20.00, "cat": "Electronics"},
    {"title": "Bose QuietComfort Ultra Headphones", "desc": "Noise cancelling, black color.", "price": 349.00, "increment": 15.00, "cat": "Electronics"},

    # Fashion
    {"title": "Gucci GG Marmont Bag", "desc": "Authentic, medium size, dustbag included.", "price": 1200.00, "increment": 50.00, "cat": "Fashion"},
    {"title": "Rolex Submariner Date", "desc": "2022, full set with papers.", "price": 12000.00, "increment": 250.00, "cat": "Fashion"},
    {"title": "Louis Vuitton Neverfull MM", "desc": "Damier Ebene, excellent condition.", "price": 950.00, "increment": 40.00, "cat": "Fashion"},
    {"title": "Nike Air Jordan 1 Retro High", "desc": "Chicago colorway, size 10, DS.", "price": 350.00, "increment": 20.00, "cat": "Fashion"},
    {"title": "Burberry Trench Coat", "desc": "Classic beige, size M, like new.", "price": 800.00, "increment": 35.00, "cat": "Fashion"},

    # Home & Garden
    {"title": "Herman Miller Aeron Chair", "desc": "Size B, fully loaded, remastered.", "price": 800.00, "increment": 30.00, "cat": "Home & Garden"},
    {"title": "Dyson V15 Detect Vacuum", "desc": "Complete with all attachments.", "price": 499.00, "increment": 20.00, "cat": "Home & Garden"},
    {"title": "KitchenAid Artisan Mixer", "desc": "Empire Red, 5-quart, barely used.", "price": 299.00, "increment": 15.00, "cat": "Home & Garden"},
    {"title": "Weber Genesis Gas Grill", "desc": "3-burner, natural gas, cover included.", "price": 699.00, "increment": 25.00, "cat": "Home & Garden"},
    {"title": "Roomba j7+ Robot Vacuum", "desc": "Self-emptying base included.", "price": 599.00, "increment": 25.00, "cat": "Home & Garden"},

    # Sports & Outdoors
    {"title": "Peloton Bike+", "desc": "Barely used, includes shoes and weights.", "price": 1800.00, "increment": 50.00, "cat": "Sports & Outdoors"},
    {"title": "Callaway Paradym Driver", "desc": "9 degree, stiff shaft, headcover.", "price": 399.00, "increment": 20.00, "cat": "Sports & Outdoors"},
    {"title": "Trek Madone SLR 7", "desc": "Size 56, Shimano Ultegra Di2.", "price": 5500.00, "increment": 100.00, "cat": "Sports & Outdoors"},
    {"title": "Yeti Tundra 65 Cooler", "desc": "White, excellent condition.", "price": 275.00, "increment": 15.00, "cat": "Sports & Outdoors"},
    {"title": "Bowflex SelectTech Dumbbells", "desc": "5-52.5 lbs pair with stand.", "price": 349.00, "increment": 20.00, "cat": "Sports & Outdoors"},

    # Collectibles & Art
    {"title": "Pokemon Base Set Charizard", "desc": "PSA 8, 1st Edition Shadowless.", "price": 15000.00, "increment": 500.00, "cat": "Collectibles & Art"},
    {"title": "Signed Michael Jordan Jersey", "desc": "UDA authenticated, framed.", "price": 3500.00, "increment": 100.00, "cat": "Collectibles & Art"},
    {"title": "Original Andy Warhol Print", "desc": "Campbell's Soup Can, numbered.", "price": 8000.00, "increment": 200.00, "cat": "Collectibles & Art"},
    {"title": "Vintage Star Wars Figures Lot", "desc": "12 figures from 1977-1983, good condition.", "price": 450.00, "increment": 25.00, "cat": "Collectibles & Art"},
    {"title": "First Edition Harry Potter Book", "desc": "Philosopher's Stone, UK hardcover.", "price": 25000.00, "increment": 500.00, "cat": "Collectibles & Art"},

    # Vehicles
    {"title": "2020 Tesla Model 3 Long Range", "desc": "White, 35k miles, FSD included.", "price": 32000.00, "increment": 500.00, "cat": "Vehicles"},
    {"title": "1967 Ford Mustang Fastback", "desc": "Restored, 289 V8, Highland Green.", "price": 75000.00, "increment": 1000.00, "cat": "Vehicles"},
    {"title": "2022 Harley-Davidson Street Glide", "desc": "Vivid Black, 5k miles, Stage 2.", "price": 22000.00, "increment": 500.00, "cat": "Vehicles"},

    # Toys & Hobbies
    {"title": "LEGO Star Wars Millennium Falcon", "desc": "UCS 75192, sealed in box.", "price": 799.00, "increment": 30.00, "cat": "Toys & Hobbies"},
    {"title": "Nintendo Switch OLED Bundle", "desc": "White, with 5 games.", "price": 399.00, "increment": 20.00, "cat": "Toys & Hobbies"},
    {"title": "Hot Wheels Collection 200+ Cars", "desc": "Vintage and modern, some rare.", "price": 500.00, "increment": 25.00, "cat": "Toys & Hobbies"},

    # Books & Media
    {"title": "Complete Beatles Vinyl Collection", "desc": "Original pressings, VG+ condition.", "price": 1200.00, "increment": 50.00, "cat": "Books & Media"},
    {"title": "Signed Stephen King First Editions", "desc": "IT, The Shining, Pet Sematary.", "price": 2500.00, "increment": 75.00, "cat": "Books & Media"},

    # Jewelry & Watches
    {"title": "Cartier Love Bracelet", "desc": "18k yellow gold, size 17, box/papers.", "price": 5500.00, "increment": 150.00, "cat": "Jewelry & Watches"},
    {"title": "Tiffany & Co Diamond Studs", "desc": "1ct total, platinum setting.", "price": 3200.00, "increment": 100.00, "cat": "Jewelry & Watches"},
    {"title": "Omega Speedmaster Moonwatch", "desc": "Hesalite crystal, 2023, full set.", "price": 5800.00, "increment": 150.00, "cat": "Jewelry & Watches"},

    # Health & Beauty
    {"title": "Dyson Airwrap Complete", "desc": "All attachments, long barrels.", "price": 499.00, "increment": 25.00, "cat": "Health & Beauty"},
    {"title": "NuFace Trinity Facial Device", "desc": "With ELE attachment, like new.", "price": 299.00, "increment": 20.00, "cat": "Health & Beauty"},
]

# Placeholder image URLs (using placeholder service)
PLACEHOLDER_IMAGES = [
    "https://placehold.co/600x400/e2e8f0/1e293b?text=Product+Image",
    "https://placehold.co/600x400/dbeafe/1e40af?text=Product+Image+2",
    "https://placehold.co/600x400/dcfce7/166534?text=Product+Image+3",
]

# Sample addresses for Turkey
SAMPLE_ADDRESSES = [
    {"title": "Home", "city": "Istanbul", "district": "Kadıköy", "full_address": "Caferağa Mah. Moda Cad. No:15 D:3", "postal_code": "34710"},
    {"title": "Work", "city": "Istanbul", "district": "Şişli", "full_address": "Mecidiyeköy Mah. Büyükdere Cad. No:100 K:5", "postal_code": "34394"},
    {"title": "Home", "city": "Ankara", "district": "Çankaya", "full_address": "Kızılay Mah. Atatürk Bulvarı No:50 D:12", "postal_code": "06420"},
    {"title": "Office", "city": "Izmir", "district": "Konak", "full_address": "Alsancak Mah. Kıbrıs Şehitleri Cad. No:25", "postal_code": "35220"},
    {"title": "Home", "city": "Istanbul", "district": "Beşiktaş", "full_address": "Levent Mah. Nispetiye Cad. No:88 D:5", "postal_code": "34340"},
    {"title": "Summer House", "city": "Antalya", "district": "Muratpaşa", "full_address": "Lara Mah. Güzeloba Cad. No:200", "postal_code": "07230"},
    {"title": "Home", "city": "Bursa", "district": "Nilüfer", "full_address": "Özlüce Mah. Atatürk Cad. No:75 D:8", "postal_code": "16120"},
    {"title": "Work", "city": "Istanbul", "district": "Sarıyer", "full_address": "Maslak Mah. Eski Büyükdere Cad. No:55", "postal_code": "34398"},
]


def clear_database(db):
    """Clear all data from database tables."""
    print("Clearing existing data...")
    db.query(Payment).delete()
    db.query(Order).delete()
    db.query(Favorite).delete()
    # Clear accepted_bid_id FK before deleting bids (circular dependency)
    db.query(Product).update({Product.accepted_bid_id: None})
    db.query(Bid).delete()
    db.query(ProductImage).delete()
    db.query(Product).delete()
    db.query(Category).delete()
    db.query(Address).delete()
    db.query(User).delete()
    db.commit()
    print("Database cleared.")


def seed_users(db) -> dict:
    """Create sample users and return a mapping of emails to user objects."""
    print("Creating users...")
    users = {}
    password_hash = get_password_hash("password123")  # Same password for all test users

    for user_data in SAMPLE_USERS:
        user = User(
            email=user_data["email"],
            password_hash=password_hash,
            full_name=user_data["full_name"],
            phone_number=user_data["phone"],
        )
        db.add(user)
        users[user_data["email"]] = user

    db.commit()
    print(f"  Created {len(users)} users.")
    return users


def seed_addresses(db, users: dict):
    """Create sample addresses for users."""
    print("Creating addresses...")
    count = 0
    address_idx = 0

    for user in users.values():
        # Each user gets 1-2 addresses
        num_addresses = random.randint(1, 2)
        for _ in range(num_addresses):
            addr_data = SAMPLE_ADDRESSES[address_idx % len(SAMPLE_ADDRESSES)]
            address = Address(
                user_id=user.id,
                title=addr_data["title"],
                city=addr_data["city"],
                district=addr_data["district"],
                full_address=addr_data["full_address"],
                postal_code=addr_data["postal_code"],
            )
            db.add(address)
            count += 1
            address_idx += 1

    db.commit()
    print(f"  Created {count} addresses.")


def seed_categories(db) -> dict:
    """Create categories and return a mapping of names to category objects."""
    print("Creating categories...")
    categories = {}

    for name in CATEGORIES:
        category = Category(name=name)
        db.add(category)
        categories[name] = category

    db.commit()
    print(f"  Created {len(categories)} categories.")
    return categories


def seed_products(db, users: dict, categories: dict) -> list:
    """Create sample products with images."""
    print("Creating products...")
    products = []
    user_list = list(users.values())

    now = datetime.utcnow()

    for i, prod_data in enumerate(SAMPLE_PRODUCTS):
        # Rotate through users as sellers
        seller = user_list[i % len(user_list)]
        category = categories[prod_data["cat"]]

        # Vary auction end times: some ended, some ending soon, some later
        if i % 5 == 0:
            # Already expired (ended yesterday)
            end_time = now - timedelta(days=1)
            status = ProductStatus.EXPIRED
        elif i % 5 == 1:
            # Ending within 24 hours
            end_time = now + timedelta(hours=random.randint(1, 23))
            status = ProductStatus.ACTIVE
        elif i % 5 == 2:
            # Ending within a week
            end_time = now + timedelta(days=random.randint(1, 7))
            status = ProductStatus.ACTIVE
        else:
            # Ending in 1-3 weeks
            end_time = now + timedelta(days=random.randint(7, 21))
            status = ProductStatus.ACTIVE

        product = Product(
            seller_id=seller.id,
            category_id=category.id,
            title=prod_data["title"],
            description=prod_data["desc"],
            starting_price=Decimal(str(prod_data["price"])),
            min_increment=Decimal(str(prod_data["increment"])),
            auction_end_at=end_time,
            status=status,
        )
        db.add(product)
        products.append(product)

    db.commit()

    # Add images to products
    print("Adding product images...")
    for product in products:
        num_images = random.randint(1, 3)
        for pos in range(num_images):
            image = ProductImage(
                product_id=product.id,
                image_url=PLACEHOLDER_IMAGES[pos % len(PLACEHOLDER_IMAGES)],
                position=pos,
            )
            db.add(image)

    db.commit()
    print(f"  Created {len(products)} products with images.")
    return products


def seed_bids(db, users: dict, products: list) -> list:
    """Create sample bids on products."""
    print("Creating bids...")
    user_list = list(users.values())
    bids = []

    for product in products:
        if product.status != ProductStatus.ACTIVE:
            continue

        # Random number of bids per product (0-5)
        num_bids = random.randint(0, 5)
        current_price = product.starting_price

        # Select random bidders (exclude the product owner)
        potential_bidders = [u for u in user_list if u.id != product.seller_id]
        bidders = random.sample(potential_bidders, min(num_bids, len(potential_bidders)))

        for i, bidder in enumerate(bidders):
            # Each bid increases by at least min_increment
            bid_amount = current_price + product.min_increment * Decimal(random.randint(1, 3))

            bid = Bid(
                product_id=product.id,
                bidder_id=bidder.id,
                amount=bid_amount,
                status=BidStatus.PENDING if i == len(bidders) - 1 else BidStatus.OUTBID,
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48)),
            )
            db.add(bid)
            bids.append(bid)
            current_price = bid_amount

    db.commit()
    print(f"  Created {len(bids)} bids.")
    return bids


def seed_favorites(db, users: dict, products: list):
    """Create sample favorites/watchlist entries."""
    print("Creating favorites...")
    user_list = list(users.values())
    count = 0

    for user in user_list:
        # Each user favorites 3-8 random products (not their own)
        num_favorites = random.randint(3, 8)
        other_products = [p for p in products if p.seller_id != user.id]
        favorite_products = random.sample(other_products, min(num_favorites, len(other_products)))

        for product in favorite_products:
            favorite = Favorite(
                user_id=user.id,
                product_id=product.id,
            )
            db.add(favorite)
            count += 1

    db.commit()
    print(f"  Created {count} favorites.")


def seed_completed_auctions(db, users: dict, products: list):
    """Create some completed auctions with orders and payments."""
    print("Creating completed auctions with orders...")
    user_list = list(users.values())

    # Find expired products and simulate completed sales
    expired_products = [p for p in products if p.status == ProductStatus.EXPIRED]
    order_count = 0

    for product in expired_products[:5]:  # Complete 5 auctions
        # Create a winning bid (from someone other than the seller)
        potential_buyers = [u for u in user_list if u.id != product.seller_id]
        buyer = random.choice(potential_buyers)
        winning_amount = product.starting_price + product.min_increment * Decimal(random.randint(3, 10))

        winning_bid = Bid(
            product_id=product.id,
            bidder_id=buyer.id,
            amount=winning_amount,
            status=BidStatus.ACCEPTED,
            created_at=product.auction_end_at - timedelta(hours=2),
        )
        db.add(winning_bid)
        db.flush()  # Get the bid ID

        # Update product
        product.status = ProductStatus.SOLD
        product.accepted_bid_id = winning_bid.id

        # Create order
        order = Order(
            product_id=product.id,
            buyer_id=buyer.id,
            seller_id=product.seller_id,
            bid_id=winning_bid.id,
            total_amount=winning_amount,
            status=OrderStatus.PAID,
        )
        db.add(order)
        db.flush()

        # Create payment
        payment = Payment(
            order_id=order.id,
            provider="MOCK",
            payment_ref=f"MOCK-{random.randint(100000, 999999)}",
            status=PaymentStatus.SUCCESS,
            paid_at=product.auction_end_at + timedelta(hours=random.randint(1, 24)),
        )
        db.add(payment)
        order_count += 1

    db.commit()
    print(f"  Created {order_count} completed orders with payments.")


def main():
    """Main seeding function."""
    print("\n" + "=" * 50)
    print("BidBay Database Seeding")
    print("=" * 50 + "\n")

    db = SessionLocal()

    try:
        # Clear existing data
        clear_database(db)

        # Seed data in order
        users = seed_users(db)
        seed_addresses(db, users)
        categories = seed_categories(db)
        products = seed_products(db, users, categories)
        seed_bids(db, users, products)
        seed_favorites(db, users, products)
        seed_completed_auctions(db, users, products)

        print("\n" + "=" * 50)
        print("Seeding completed successfully!")
        print("=" * 50)
        print("\nTest Credentials (all users have password: password123):")
        print("  - user1@bidbay.com")
        print("  - user2@bidbay.com")
        print("  - ... up to user13@bidbay.com")
        print("  - admin@bidbay.com")
        print()

    except Exception as e:
        print(f"\nError during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
