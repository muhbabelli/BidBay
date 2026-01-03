# BidBay Frontend (Minimal Demo)

This frontend is a lightweight HTML+JS demo to verify the backend works. It uses the local API at `http://localhost:8000` and a static server for the HTML files.

## Prerequisites

- Backend running on `http://localhost:8000`
- Seeded DB (optional but recommended) so you have products and bids

## Start the frontend server

From the project root:

```bash
cd /Users/gulara/BidBay/frontend
python -m http.server 5173
```

Then open:

- `http://localhost:5173/login.html`
- `http://localhost:5173/products.html`

## Login

Use a seeded account (password: `password123`):

- Buyer: `buyer1@bidbay.com`
- Seller: `seller3@bidbay.com`

## Products page

- Click a product card to see details.
- Sellers can see current bids for their own products.
- Buyers can place a bid.

## Troubleshooting

- If login succeeds but products say "Not logged in", clear storage and log in again.
- If products fail to load, ensure the backend is running and reachable at `http://localhost:8000`.
