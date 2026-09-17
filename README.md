# SupplyLedger — Inventory & Sales Management System

SupplyLedger is a full-stack inventory and sales management system for small businesses. It helps users manage products, suppliers, purchases, sales, stock levels, and business insights from one application.

## Features

- JWT-based authentication with admin, manager, and cashier roles
- Product and category management
- Supplier management
- Purchase / Stock In with multiple products
- Sales / Stock Out with multiple products
- Automatic stock updates after purchases and sales
- Low-stock tracking and alerts
- Dashboard with monthly sales, stock value, sales trends, and top products
- Customer selection and creation during sales
- Role-aware frontend controls

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, React Router, Axios, Chart.js |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL |
| Authentication | JWT and bcrypt |
| Database environment | Docker Compose |

## Project Structure

```text
inventory-sales-/
├── backend/        FastAPI backend and REST API
├── db/             PostgreSQL schema and seed data
├── frontend/       React + Vite frontend
├── docs/           Project setup notes
├── docker-compose.yml
└── README.md
```

## Prerequisites

Install the following before running the project:

- Git
- Docker Desktop
- Python 3.11 or newer
- Node.js 20 or newer

## Run the Project

Use three PowerShell windows and keep them open while using the application.

### 1. Start PostgreSQL

From the project root:

```powershell
cd "C:\path\to\inventory-sales-"
docker compose up -d
```

To confirm that PostgreSQL is running:

```powershell
docker compose ps
```

### 2. Start the FastAPI Backend

Open a new PowerShell window:

```powershell
cd "C:\path\to\inventory-sales-\backend"
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --app-dir .
```

The backend will run at:

```text
http://localhost:8000
```

FastAPI API documentation is available at:

```text
http://localhost:8000/docs
```

### 3. Start the React Frontend

Open another PowerShell window:

```powershell
cd "C:\path\to\inventory-sales-\frontend"
Copy-Item .env.example .env
npm install
npm run dev
```

Open the address shown in the terminal, normally:

```text
http://localhost:5173
```

## First-Time Setup

The database is initially empty.

1. Open the frontend in the browser.
2. Select **Register** and create the first account.
3. The first registered account automatically becomes an admin.
4. Add categories and suppliers.
5. Add products.
6. Create a purchase to add stock.
7. Create a sale to reduce stock.
8. View stock status and dashboard insights.

## Roles and Permissions

| Action | Admin | Manager | Cashier |
|---|---:|---:|---:|
| Manage products, categories, suppliers | Yes | Yes | No |
| Create purchases / stock in | Yes | Yes | No |
| Create and update customers | Yes | Yes | Yes |
| Create sales / stock out | Yes | Yes | Yes |
| View products, purchases, sales, stock, dashboard | Yes | Yes | Yes |

## Stock Rules

- Products begin with stock quantity `0`.
- Product stock cannot be edited directly from the product form.
- Purchases increase stock.
- Sales decrease stock.
- The backend rejects a sale when the requested quantity exceeds available stock.
- Products at or below their low-stock threshold appear as low-stock items.

## Stopping the Project

To stop the frontend or backend, press `Ctrl + C` in their respective PowerShell windows.

To stop PostgreSQL:

```powershell
cd "C:\path\to\inventory-sales-"
docker compose down
```

This stops the database while preserving its existing data.

## Team Responsibilities

| Area | Responsibility |
|---|---|
| Database | PostgreSQL schema, constraints, seed data |
| Backend | FastAPI routes, authentication, stock transactions |
| Frontend | React UI, forms, routing, API integration, dashboard |

## License

This project was created for academic purposes.