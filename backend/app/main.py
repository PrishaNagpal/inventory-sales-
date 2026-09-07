from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.config import settings
from app.models import *  # noqa: F401,F403 — register models with SQLAlchemy
from app.routers.auth import router as auth_router
from app.routers.categories import router as categories_router
from app.routers.customers import router as customers_router
from app.routers.dashboard import router as dashboard_router
from app.routers.orders import router as orders_router
from app.routers.products import router as products_router
from app.routers.purchases import router as purchases_router
from app.routers.suppliers import router as suppliers_router

app = FastAPI(
    title="Inventory & Sales API",
    version="0.1.0",
    description="Backend for the inventory and sales management system. Purchases, sales, and dashboard included.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(suppliers_router, prefix="/suppliers", tags=["Suppliers"])
app.include_router(customers_router, prefix="/customers", tags=["Customers"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(purchases_router, prefix="/purchases", tags=["Purchases"])
app.include_router(orders_router, prefix="/orders", tags=["Sales"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])


@app.exception_handler(OperationalError)
def database_unavailable(_request: Request, _exc: OperationalError):
    return JSONResponse(
        status_code=503,
        content={
            "detail": "PostgreSQL is not running. Start the database, then try again."
        },
    )


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
