# Inventory & Sales Management System

Team project: inventory tracking, purchases, sales, and reports.

| Role | Owns |
|------|------|
| Database | PostgreSQL schema, seed data, views/triggers (`/db`) |
| Backend | FastAPI APIs (`/backend`) |
| Frontend | React UI (`/frontend`) |

## Repo layout

```
inventory-sales/
  db/          PostgreSQL schema, seed, ERD
  backend/     FastAPI
  frontend/    React (Vite)
  docs/        Setup notes and API/schema notes
```

## Run locally (once each part exists)

1. Start Postgres: `docker compose up -d`
2. Backend: see `backend/README.md`
3. Frontend: see `frontend/README.md`

## Working together

- `main` should always be runnable.
- Schema changes go in `/db` first, then backend, then frontend.
- Do not commit `.env` files. Copy `.env.example` instead.
