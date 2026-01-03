# BidBay – Auction & Bidding Marketplace Web Application

BidBay is a full-stack auction-based marketplace web application inspired by platforms like eBay.
It allows sellers to list products and buyers to place bids, track their offers, and complete purchases through a mock payment system.

---

## 🚀 Features

### Buyer

* Register & login
* Browse and search products
* View product details and images
* Add/remove products from favorites
* Place bids on active products
* View all bids placed with status (Pending / Accepted / Rejected / Outbid)
* Complete mock payment for accepted bids

### Seller

* Register & login
* Create, update, and delete product listings
* Upload product images
* View bids on own products
* Accept or reject bids
* Track payment status after accepting a bid

### System

* Role-based authentication (Buyer / Seller)
* Relational MySQL database
* Transaction-safe bidding logic
* Advanced SQL queries integrated into the system
* Mock payment flow (no real payment processing)

---

## 🛠️ Tech Stack

### Backend

* **Python 3.10**
* **FastAPI**
* **SQLAlchemy (ORM)**
* **Alembic (migrations)**
* **MySQL**
* JWT-based authentication

### Frontend

* **React** (separate repository / folder)
* REST API communication

---

## 📁 Project Structure (Backend)

```
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   ├── schemas/
│   ├── api/
│   ├── seed.py
│   └── utils/
├── alembic/
├── alembic.ini
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Environment Setup

## Clone Repository
```bash
git clone https://github.com/muhbabelli/BidBay.git
```


### 1️⃣ Create Conda Environment

```bash
conda create -n bidbay python=3.10 -y
conda activate bidbay
```

### 2️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🗄️ Database Setup (MySQL)

### 1️⃣ Create Database

```sql
CREATE DATABASE bidbay CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2️⃣ Configure Environment Variables

Create a `.env` file in the backend root:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/bidbay
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 🔄 Database Migrations

### Initialize Alembic (first time only)

```bash
alembic init alembic
```

### Generate Migration

```bash
alembic revision --autogenerate -m "initial schema"
```

### Apply Migration

```bash
alembic upgrade head
```

---

## 🌱 Seed Database (Optional but Recommended)

Populate the database with sample users, products, bids, and favorites:

```bash
python -m scripts.seed
```

This creates realistic demo data for testing and showcasing advanced SQL queries.

---

## ▶️ Run Backend Server

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## 📊 Advanced SQL Queries (Integrated)

The system includes advanced SQL queries such as:

* Ending-soon auctions
* Seller dashboards with bid statistics
* Trending products by favorites
* Buyer bid analytics
* Outbid detection

These queries are implemented using SQLAlchemy and/or raw SQL and integrated into API endpoints.

---

## 💳 Payment Handling

Payments are **mocked** for demonstration purposes.

* No real payment gateway is used
* Successful payment updates order and product status

---

## 🔐 Security Notes

* Passwords are hashed using bcrypt
* JWT authentication
* Role-based access control
* Input validation via Pydantic
* Transaction-safe bid placement


## 👨‍💻 Authors

Developed as part of a university project for database-driven web applications.
