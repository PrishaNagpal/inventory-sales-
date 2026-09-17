# SupplyLedger Frontend

The SupplyLedger frontend is a React and Vite application for managing inventory, suppliers, purchases, sales, stock levels, and dashboard insights.

It communicates with the FastAPI backend through REST APIs.

## Tech Stack

- React
- Vite
- React Router
- Axios
- Chart.js
- Lucide React
- Plain CSS

## Features

- Login, registration, logout, and protected routes
- JWT token handling
- Role-aware interface for admin, manager, and cashier accounts
- Responsive charcoal, cream, terracotta, sage, and amber dashboard design
- Product listing, search, filtering, creation, editing, and deletion
- Category and supplier management
- Multi-item purchase form for stock-in
- Multi-item sales form for stock-out
- Customer selection and quick customer creation during sales
- Stock tracking with low-stock and out-of-stock indicators
- Dashboard cards, sales chart, top products, and low-stock list
- Loading, error, validation, success, and empty states

## Folder Structure

```text
frontend/
├── src/
│   ├── api/           API client and backend requests
│   ├── auth/          Authentication context
│   ├── components/    Shared layout and UI components
│   ├── pages/         Application pages
│   ├── styles.css     Global styles and design tokens
│   ├── App.jsx        Routes and application structure
│   └── main.jsx       React entry point
├── .env.example       Frontend environment variable example
├── package.json
└── vite.config.js
```

## Prerequisites

- Node.js 20 or newer
- npm
- The FastAPI backend running at `http://localhost:8000`

## Environment Setup

Create a `.env` file in the `frontend` folder.

```powershell
Copy-Item .env.example .env
```

The file should contain:

```text
VITE_API_URL=http://localhost:8000
```

Do not commit `.env` to GitHub.

## Install and Run

From the `frontend` folder:

```powershell
npm install
npm run dev
```

Vite will display a local URL, normally:

```text
http://localhost:5173
```

Open that address in a browser.

## Available Scripts

### Start development server

```powershell
npm run dev
```

### Create production build

```powershell
npm run build
```

### Preview production build locally

```powershell
npm run preview
```

## Backend Requirement

The backend and PostgreSQL database must be running for login and data-related features to work.

From the project root, start PostgreSQL:

```powershell
docker compose up -d
```

From the `backend` folder, start FastAPI:

```powershell
uvicorn app.main:app --reload --app-dir .
```

## Main Application Pages

| Route | Purpose |
|---|---|
| `/login` | Sign in to an existing account |
| `/register` | Register a new account |
| `/dashboard` | View sales, stock, low-stock, and top-product insights |
| `/products` | Manage products and product details |
| `/categories` | Manage product categories |
| `/suppliers` | Manage suppliers |
| `/purchases` | Record stock-in purchases |
| `/sales` | Record stock-out sales |
| `/stock` | Track stock quantities and low-stock items |

## Notes

- Categories and suppliers must be created before they appear in the Add Product form.
- Products start with zero stock.
- Use Purchases to increase stock.
- Use Sales to decrease stock.
- The frontend validates forms, but the backend makes the final stock and authorization decisions.
- The first registered account is created as an admin by the backend.

## Troubleshooting

### The page loads but login or data does not work

Confirm the backend is running at:

```text
http://localhost:8000
```

### Category or supplier dropdown is empty

Create categories and suppliers first through their corresponding pages, then reopen the Add Product form.

### `npm` is not recognized

Install Node.js, restart PowerShell, and run the commands again.

### Backend returns a database error

Start Docker Desktop, then run this from the project root:

```powershell
docker compose up -d
```