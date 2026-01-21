# BidBay – Auction & Bidding Marketplace Web Application

BidBay is a full-stack auction-based marketplace web application inspired by platforms like eBay. It allows users to list products, place bids, track offers, manage favorites, and complete purchases through a mock payment system.

![BidBay ER Diagram](Documentation/ER-Diagram.jpeg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Database Schema](#-database-schema)
- [Project Structure](#-project-structure)
- [Installation Guide](#-installation-guide)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Application](#-running-the-application)
- [Advanced SQL Queries](#-advanced-sql-queries)
- [API Documentation](#-api-documentation)
- [Security Features](#-security-features)
- [Authors](#-authors)

---

## 🚀 Features

### User Management

* User registration and authentication with email/password
* Profile management with profile picture upload (base64 image storage)
* View and edit personal information (name, phone number)
* Default profile image for new users
* Secure JWT-based authentication with bcrypt password hashing

### Buyer Features

* Browse and search products in real-time with dynamic search
* View detailed product information with high-quality images
* Add/remove products from favorites list
* Place bids on active auctions with smart validation
* Automatic bid validation with minimum increment enforcement
* Smart bid input defaults (starts at minimum required bid)
* View all placed bids with real-time status tracking (Pending / Accepted / Rejected / Outbid)
* Receive seller contact information upon bid acceptance
* Complete mock payment for accepted bids
* View bid history with timestamps

### Seller Features

* Create product listings with image upload (supports PNG, JPG)
* Set starting price, minimum bid increment, and auction end time
* View all bids on owned products with bidder information
* Accept or reject bids in real-time
* View comprehensive product statistics (highest bid, bid count, auction status)
* Monitor active and sold products
* Delete owned product listings
* Track payment status after accepting bids
* View bidder contact information for accepted bids

### System Features

* Single-tier user system (users can be both buyers and sellers)
* Relational MySQL database with comprehensive normalized schema
* Transaction-safe bidding logic with automatic status updates
* Advanced SQL queries integrated into analytics endpoints
* Real-time bid validation with minimum increment enforcement
* Timezone-aware timestamps (UTC storage, automatic local display)
* Responsive React frontend with modern UI/UX
* Mock payment flow (no real payment processing)
* Automatic bid status management (PENDING → ACCEPTED/REJECTED/OUTBID)
* Product status management (ACTIVE → SOLD)

---

## 🛠️ Tech Stack

### Backend

* **Python 3.10+**
* **FastAPI** - Modern, fast web framework for building APIs
* **SQLAlchemy 2.0** - SQL toolkit and ORM
* **Alembic** - Database migration tool
* **MySQL 8.0+** - Relational database
* **PyMySQL** - MySQL driver for Python
* **Pydantic** - Data validation using Python type annotations
* **python-jose** - JWT token implementation
* **passlib & bcrypt** - Password hashing
* **python-multipart** - File upload support

### Frontend

* **React 18** - JavaScript library for building user interfaces
* **Vite** - Next-generation frontend build tool
* **JavaScript (ES6+)** - Modern JavaScript features
* **CSS3** - Custom styling with CSS variables
* **REST API** - Communication with backend

### Development Tools

* **Uvicorn** - ASGI server for FastAPI
* **Conda** - Package and environment management
* **Git** - Version control

---

## 🗄️ Database Schema

BidBay uses a comprehensive relational database schema with 9 entities:

### Entities

1. **Users** - User accounts with authentication credentials and profile information
2. **Products** - Auction listings with pricing and timing information
3. **Product Images** - Multiple images per product with position ordering
4. **Bids** - Bid records with amount and status tracking
5. **Favorites** - User's favorited products
6. **Orders** - Purchase orders created from accepted bids
7. **Payments** - Payment records for orders
8. **Categories** - Product categorization (optional)
9. **Reviews** - Product reviews (optional)

### Key Relationships

* One-to-Many: User → Products (seller relationship)
* One-to-Many: Product → Bids
* One-to-Many: Product → Product Images
* Many-to-Many: User ↔ Products (via Favorites)
* One-to-One: Bid → Order (for accepted bids)
* One-to-One: Order → Payment

For detailed ER diagram, see [Documentation/ER-Diagram.jpeg](Documentation/ER-Diagram.jpeg)

---

## 📁 Project Structure

```
BidBay/
├── app/                          # Backend application
│   ├── main.py                   # FastAPI application entry point
│   ├── core/                     # Core configurations
│   │   ├── config.py             # Environment configuration
│   │   ├── database.py           # Database connection setup
│   │   └── security.py           # JWT and password hashing
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── bid.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   └── ...
│   ├── schemas/                  # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── bid.py
│   │   └── ...
│   ├── api/                      # API route handlers
│   │   ├── __init__.py
│   │   ├── deps.py               # Dependency injection
│   │   ├── auth.py               # Authentication endpoints
│   │   ├── products.py           # Product CRUD operations
│   │   ├── bids.py               # Bidding operations
│   │   ├── favorites.py          # Favorites management
│   │   ├── orders.py             # Order management
│   │   ├── payments.py           # Payment processing
│   │   └── analytics.py          # Advanced SQL queries
│   └── utils/                    # Utility functions
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration scripts
│   └── env.py                    # Alembic configuration
├── scripts/                      # Utility scripts
│   └── seed.py                   # Database seeding script
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Feed.jsx
│   │   │   ├── Home.jsx
│   │   │   ├── Favorites.jsx
│   │   │   ├── ProductModal.jsx
│   │   │   ├── MyProductModal.jsx
│   │   │   ├── CreateProductModal.jsx
│   │   │   ├── ProfileModal.jsx
│   │   │   └── ...
│   │   ├── services/             # API service layer
│   │   │   └── api.js
│   │   ├── App.jsx               # Main React component
│   │   ├── main.jsx              # React entry point
│   │   └── ...
│   ├── public/                   # Static assets
│   ├── index.html                # HTML entry point
│   ├── package.json              # NPM dependencies
│   └── vite.config.js            # Vite configuration
├── Documentation/                # Project documentation
│   ├── ER-Diagram.jpeg           # Database ER diagram
│   └── BidBay_Project_Report.tex # LaTeX project report
├── tests/                        # Test suite
├── .env                          # Environment variables (not in git)
├── .gitignore                    # Git ignore rules
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 📥 Installation Guide

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
* **MySQL 8.0 or higher** - [Download MySQL](https://dev.mysql.com/downloads/)
* **Node.js 18+ and npm** - [Download Node.js](https://nodejs.org/)
* **Conda** (recommended) - [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html)
* **Git** - [Download Git](https://git-scm.com/downloads)

### Backend Setup

#### 1. Clone Repository

```bash
git clone https://github.com/muhbabelli/BidBay.git
cd BidBay
```

#### 2. Create and Activate Conda Environment

```bash
conda create -n bidbay python=3.10 -y
conda activate bidbay
```

#### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Create MySQL Database

Open MySQL command line or workbench and execute:

```sql
CREATE DATABASE bidbay CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 5. Configure Environment Variables

Create a `.env` file in the project root directory:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://your_username:your_password@localhost:3306/bidbay

# Security Configuration
SECRET_KEY=your-secret-key-here-generate-a-strong-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Optional: API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=BidBay
```

Replace `your_username` and `your_password` with your MySQL credentials.

To generate a secure SECRET_KEY, you can use:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 6. Initialize Database Schema

Run Alembic migrations to create all tables:

```bash
# The alembic directory is already initialized, so just run migrations
alembic upgrade head
```

This will create all necessary tables based on the SQLAlchemy models.

#### 7. Seed Database (Optional but Recommended)

Populate the database with sample data for testing:

```bash
python -m scripts.seed
```

This creates:
- Sample user accounts
- Product listings with images
- Bids on various products
- Favorite products
- Sample orders and payments

**Test Users Created:**
- Email: `alice@example.com` / Password: `password123`
- Email: `bob@example.com` / Password: `password123`
- Email: `charlie@example.com` / Password: `password123`
- And more...

### Frontend Setup

#### 1. Navigate to Frontend Directory

```bash
cd frontend
```

#### 2. Install Node Dependencies

```bash
npm install
```

This will install all required dependencies including React, Vite, and other packages.

#### 3. Configure API Endpoint (if needed)

The frontend is configured to communicate with the backend at `http://localhost:8000`. If your backend runs on a different port, update the API base URL in:

```javascript
// frontend/src/services/api.js
const API_BASE_URL = 'http://localhost:8000';
```

---

## ▶️ Running the Application

### Start Backend Server

From the project root directory with conda environment activated:

```bash
uvicorn app.main:app --reload
```

The backend API will be available at:
- API: `http://localhost:8000`
- Interactive API Documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API Documentation (ReDoc): `http://localhost:8000/redoc`

### Start Frontend Development Server

In a new terminal, navigate to the frontend directory:

```bash
cd frontend
npm run dev
```

The frontend will be available at:
- Frontend: `http://localhost:5173`

### Access the Application

1. Open your browser and go to `http://localhost:5173`
2. You'll see the landing page with Login and Sign Up buttons
3. Sign up for a new account or use one of the seeded accounts
4. Start exploring the marketplace!

---

## 📊 Advanced SQL Queries

BidBay includes several advanced SQL queries implemented in the `/analytics` endpoints:

### 1. Trending Products

```sql
SELECT
    Product.id,
    Product.title,
    COUNT(Favorite.product_id) as favorite_count
FROM products Product
JOIN favorites Favorite ON Favorite.product_id = Product.id
GROUP BY Product.id
HAVING COUNT(Favorite.product_id) >= 2
ORDER BY favorite_count DESC;
```

**Endpoint:** `GET /analytics/trending-products?min_favorites=2`

### 2. Seller Bid Statistics

```sql
SELECT
    Product.id as product_id,
    Product.title,
    COUNT(Bid.id) as bid_count,
    MAX(Bid.amount) as max_bid,
    AVG(Bid.amount) as avg_bid
FROM products Product
JOIN bids Bid ON Bid.product_id = Product.id
WHERE Product.seller_id = :current_user_id
GROUP BY Product.id
HAVING COUNT(Bid.id) >= 1
ORDER BY bid_count DESC;
```

**Endpoint:** `GET /analytics/seller-bid-stats`

### 3. Outbid Detection (Subquery)

```sql
WITH max_bids AS (
    SELECT product_id, MAX(amount) as max_amount
    FROM bids
    GROUP BY product_id
)
SELECT
    Bid.id,
    Bid.product_id,
    Bid.amount,
    max_bids.max_amount
FROM bids Bid
JOIN max_bids ON Bid.product_id = max_bids.product_id
WHERE Bid.bidder_id = :current_user_id
  AND Bid.amount < max_bids.max_amount
ORDER BY max_bids.max_amount DESC;
```

**Endpoint:** `GET /analytics/outbid-bids`

### 4. Active Products Without Bids (Correlated Subquery)

```sql
SELECT
    Product.id,
    Product.title,
    Product.auction_end_at
FROM products Product
WHERE Product.status = 'ACTIVE'
  AND NOT EXISTS (
      SELECT 1 FROM bids Bid
      WHERE Bid.product_id = Product.id
  )
ORDER BY Product.auction_end_at ASC;
```

**Endpoint:** `GET /analytics/active-without-bids`

### 5. Top Bidders Leaderboard

```sql
SELECT
    User.id as user_id,
    User.email,
    COUNT(Bid.id) as bid_count
FROM users User
JOIN bids Bid ON Bid.bidder_id = User.id
GROUP BY User.id
HAVING COUNT(Bid.id) >= 2
ORDER BY bid_count DESC;
```

**Endpoint:** `GET /analytics/top-bidders?min_bids=2`

All queries demonstrate:
- **JOIN** operations across multiple tables
- **GROUP BY** with aggregate functions (COUNT, MAX, AVG)
- **HAVING** clause for post-aggregation filtering
- **Subqueries and CTEs** for complex logic
- **EXISTS** for correlated subqueries
- **ORDER BY** for result sorting

---

## 📚 API Documentation

### Authentication Endpoints

* `POST /auth/register` - Register a new user
* `POST /auth/login` - Login and receive JWT token
* `GET /auth/me` - Get current user information
* `PATCH /auth/me` - Update current user profile
* `POST /auth/logout` - Logout (client-side token removal)

### Product Endpoints

* `GET /products` - List all products with search and filters
* `GET /products/{id}` - Get product details
* `POST /products` - Create a new product (authenticated)
* `PATCH /products/{id}` - Update product (owner only)
* `DELETE /products/{id}` - Delete product (owner only)
* `GET /products/my-products` - Get current user's products

### Bid Endpoints

* `POST /bids` - Place a bid on a product
* `GET /bids/me` - Get all bids placed by current user
* `GET /bids/product/{product_id}` - Get all bids for a product (owner only)
* `POST /bids/{bid_id}/accept` - Accept a bid (creates order)
* `POST /bids/{bid_id}/reject` - Reject a bid

### Favorite Endpoints

* `GET /favorites` - Get current user's favorite products
* `POST /favorites` - Add product to favorites
* `DELETE /favorites/{product_id}` - Remove product from favorites

### Order Endpoints

* `GET /orders/buyer` - Get orders as a buyer
* `GET /orders/seller` - Get orders as a seller
* `GET /orders/{id}` - Get order details

### Payment Endpoints

* `POST /payments` - Process a mock payment for an order
* `GET /payments/{order_id}` - Get payment details for an order

### Analytics Endpoints

* `GET /analytics/trending-products` - Get trending products by favorites
* `GET /analytics/seller-bid-stats` - Get bid statistics for seller's products
* `GET /analytics/outbid-bids` - Find user's bids that were outbid
* `GET /analytics/active-without-bids` - Get active products with no bids
* `GET /analytics/top-bidders` - Get top bidders leaderboard

For detailed request/response schemas, visit the Swagger UI at `http://localhost:8000/docs` after starting the backend.

---

## 🔐 Security Features

### Authentication & Authorization

* **JWT Token Authentication** - Secure token-based authentication
* **Password Hashing** - Bcrypt hashing with salt for password storage
* **Token Expiration** - Configurable token expiration time
* **Protected Endpoints** - Role-based access control for sensitive operations

### Data Validation

* **Pydantic Models** - Strong type checking and validation
* **SQL Injection Prevention** - SQLAlchemy ORM prevents SQL injection
* **Input Sanitization** - All user inputs validated before processing

### Business Logic Security

* **Bid Validation** - Ensures bids meet minimum requirements
* **Ownership Checks** - Users can only modify their own resources
* **Status Validation** - Prevents invalid state transitions
* **Transaction Safety** - Database transactions ensure data consistency

### Best Practices

* **Environment Variables** - Sensitive data stored in .env file
* **CORS Configuration** - Proper CORS headers for API security
* **Error Handling** - Generic error messages to prevent information leakage
* **Rate Limiting** - Consider adding rate limiting for production use

---

## 💳 Payment Handling

Payments are **mocked** for demonstration purposes:

* No real payment gateway integration
* Mock payment flow simulates successful transactions
* Payment records created in database for tracking
* Order status updated upon successful payment
* Suitable for development and demonstration only

For production deployment, integrate with real payment providers like Stripe, PayPal, or similar services.

---

## 🧪 Testing

### Manual Testing

1. Use the Swagger UI at `http://localhost:8000/docs` to test API endpoints
2. Use the React frontend to test user workflows
3. Check database state using MySQL Workbench or command line

### Test Data

The seed script creates comprehensive test data including:
- Multiple user accounts with various roles
- Products in different states (active, sold)
- Bids with different statuses
- Favorites and orders
- Complete auction workflows

---

## 🚀 Deployment Considerations

For production deployment:

1. **Database**: Use a production MySQL instance with regular backups
2. **Environment**: Set strong SECRET_KEY and secure database credentials
3. **HTTPS**: Deploy behind HTTPS with valid SSL certificates
4. **CORS**: Configure CORS to allow only specific origins
5. **Rate Limiting**: Implement rate limiting to prevent abuse
6. **Monitoring**: Add logging and monitoring for production issues
7. **Static Files**: Serve React build files through a CDN or nginx
8. **Database Connection Pooling**: Configure SQLAlchemy connection pooling

---

## 🤝 Contributing

This is a university project. Contributions are limited to project team members.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Authors

Developed as part of COMP 306 - Database Management Systems course project at Koç University.

**Team Members:**
- [Your Name]
- [Team Member Names]

**Course:** COMP 306 - Database Management Systems
**Institution:** Koç University
**Academic Year:** 2024-2025 Fall

---

## 📞 Support

For questions or issues:
1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the [Project Report](Documentation/BidBay_Project_Report.tex)
3. Contact the development team

---

## 🙏 Acknowledgments

* FastAPI documentation and community
* React and Vite documentation
* SQLAlchemy documentation
* Course instructors and teaching assistants
* All open-source libraries used in this project
