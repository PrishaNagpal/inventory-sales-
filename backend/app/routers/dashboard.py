from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import Date, cast, func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Order, OrderItem, Product, User
from app.schemas.dashboard import DashboardOut, SalesPoint, TopProduct
from app.schemas.product import ProductOut

router = APIRouter()


@router.get("/", response_model=DashboardOut)
def get_dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)

    total_sales = db.scalar(
        select(func.coalesce(func.sum(Order.total_amount), 0)).where(
            Order.status == "Completed",
            Order.order_date >= month_start,
        )
    )
    stock_value = db.scalar(
        select(
            func.coalesce(func.sum(Product.cost_price * Product.stock_quantity), 0)
        )
    )
    low_stock = db.scalars(
        select(Product)
        .where(Product.stock_quantity <= Product.low_stock_threshold)
        .order_by(Product.name)
    ).all()

    trend_rows = db.execute(
        select(
            cast(Order.order_date, Date).label("day"),
            func.coalesce(func.sum(Order.total_amount), 0).label("total"),
        )
        .where(Order.status == "Completed", Order.order_date >= week_ago)
        .group_by(cast(Order.order_date, Date))
        .order_by(cast(Order.order_date, Date))
    ).all()

    qty_sold = func.coalesce(func.sum(OrderItem.quantity), 0)
    top_rows = db.execute(
        select(Product.product_id, Product.name, qty_sold.label("qty"))
        .join(OrderItem, OrderItem.product_id == Product.product_id)
        .join(Order, Order.order_id == OrderItem.order_id)
        .where(Order.status == "Completed")
        .group_by(Product.product_id, Product.name)
        .order_by(qty_sold.desc())
        .limit(5)
    ).all()

    return DashboardOut(
        total_sales_this_month=Decimal(total_sales),
        total_stock_value=Decimal(stock_value),
        low_stock_items=[ProductOut.model_validate(p) for p in low_stock],
        sales_last_7_days=[
            SalesPoint(day=row.day, total=Decimal(row.total)) for row in trend_rows
        ],
        top_products=[
            TopProduct(
                product_id=row.product_id,
                name=row.name,
                quantity_sold=int(row.qty),
            )
            for row in top_rows
        ],
    )
