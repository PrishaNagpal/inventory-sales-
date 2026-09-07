from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.product import ProductOut


class SalesPoint(BaseModel):
    day: date
    total: Decimal


class TopProduct(BaseModel):
    product_id: int
    name: str
    quantity_sold: int


class DashboardOut(BaseModel):
    total_sales_this_month: Decimal
    total_stock_value: Decimal
    low_stock_items: list[ProductOut]
    sales_last_7_days: list[SalesPoint]
    top_products: list[TopProduct]
