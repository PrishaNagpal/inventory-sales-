# Backend (FastAPI)

Owner: REST APIs, auth, and later stock transactions.

## Stack

- FastAPI — HTTP routes + automatic docs at `/docs`
- Pydantic — request/response validation
- SQLAlchemy 2 — Python classes mapped to PostgreSQL tables
- JWT + bcrypt — login tokens and password hashing

Tables are created by `db/schema.sql`, not by SQLAlchemy. Models must match that file.

## Setup

```powershell
cd C:\Users\LENOVO\Downloads\inventory-sales\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Postgres must be running with `schema.sql` already applied.

```powershell
uvicorn app.main:app --reload --app-dir .
```

Open http://localhost:8000/docs

## What works now

- `POST /auth/register` — first user becomes **admin**, later users **cashier**
- `POST /auth/login` — JSON, for React
- `POST /auth/token` — form, for Swagger Authorize
- `GET /auth/me`
- CRUD: `/categories`, `/suppliers`, `/customers`, `/products`
- `POST /purchases` — stock in (increases quantity)
- `POST /orders` — sale / stock out (decreases quantity; rejects if not enough)
- `GET /dashboard` — month sales, stock value, low stock, 7-day trend, top products

## Roles

| Role | Products / suppliers / purchases | Customers | Sales (`/orders`) |
|------|----------------------------------|-----------|-------------------|
| admin, manager | write | yes | yes |
| cashier | read | create/update | yes |
