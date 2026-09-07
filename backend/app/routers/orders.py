from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.models import Customer, Order, OrderItem, Product, User
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter()
can_sell = require_roles("admin", "manager", "cashier")


@router.get("/", response_model=list[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.order_date.desc())
    )
    return db.scalars(stmt).all()


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    order = db.scalar(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.order_id == order_id)
    )
    if order is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return order


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    body: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_sell),
):
    """Stock out: reject if not enough stock, else insert sale and decrease quantity.
    Selling price is taken from the product row, not from the client."""
    if body.customer_id is not None and db.get(Customer, body.customer_id) is None:
        raise HTTPException(status_code=400, detail="Customer not found")

    order = Order(
        customer_id=body.customer_id,
        processed_by_user_id=current_user.user_id,
        status="Completed",
        total_amount=Decimal("0"),
    )
    db.add(order)
    db.flush()

    total = Decimal("0")
    for line in body.items:
        product = db.scalar(
            select(Product)
            .where(Product.product_id == line.product_id)
            .with_for_update()
        )
        if product is None:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Product {line.product_id} not found",
            )
        if product.stock_quantity < line.quantity:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Not enough stock for '{product.name}' "
                    f"(have {product.stock_quantity}, need {line.quantity})"
                ),
            )
        db.add(
            OrderItem(
                order_id=order.order_id,
                product_id=product.product_id,
                quantity=line.quantity,
                unit_price=product.selling_price,
            )
        )
        product.stock_quantity -= line.quantity
        total += product.selling_price * line.quantity

    order.total_amount = total
    db.commit()
    db.refresh(order)
    db.refresh(order, attribute_names=["items"])
    return order
