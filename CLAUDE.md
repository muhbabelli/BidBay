# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BidBay is a FastAPI-based auction marketplace backend with MySQL database. It supports two user roles (Buyer/Seller) with features like bidding, favorites, and mock payments.

## Common Commands

```bash
# Create and activate conda environment
conda create -n bidbay python=3.10 -y
conda activate bidbay

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head

# Seed the database with sample data
python -m app.seed
```

## Architecture

### Tech Stack
- **Framework**: FastAPI with Pydantic validation
- **ORM**: SQLAlchemy 2.0
- **Database**: MySQL (via PyMySQL)
- **Auth**: JWT tokens with bcrypt password hashing
- **Migrations**: Alembic

### Planned Structure
```
app/
├── main.py           # FastAPI app entry point
├── core/
│   ├── config.py     # Settings from .env
│   ├── database.py   # SQLAlchemy engine/session
│   └── security.py   # JWT and password utils
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic request/response schemas
├── api/              # Route handlers
├── seed.py           # Database seeder
└── utils/
```

### Key Patterns
- Role-based access control (Buyer/Seller)
- Transaction-safe bidding logic
- Advanced SQL queries for analytics (ending-soon auctions, seller dashboards, trending products)

## Environment Variables

Required in `.env`:
- `DATABASE_URL` - MySQL connection string
- `SECRET_KEY` - JWT signing key
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

## API Documentation

When running, Swagger UI is available at `http://localhost:8000/docs`
