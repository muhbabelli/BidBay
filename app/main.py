from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, addresses, analytics, bids, categories, favorites, orders, payments, products

app = FastAPI(
    title="BidBay API",
    description="Auction & Bidding Marketplace API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(addresses.router)
app.include_router(analytics.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(bids.router)
app.include_router(favorites.router)
app.include_router(orders.router)
app.include_router(payments.router)


@app.get("/")
def root():
    return {"message": "BidBay API", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
