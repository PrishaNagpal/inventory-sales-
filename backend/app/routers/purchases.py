from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.models import Product, Purchase, PurchaseItem, Supplier, User
from app.schemas.purchase import PurchaseCreate, PurchaseOut

router = APIRouter()
can_buy = require_roles("admin", "manager")


@router.get("/", response_model=list[PurchaseOut])
def list_purchases(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stmt = (
        select(Purchase)
        .options(selectinload(Purchase.items))
        .order_by(Purchase.purchase_date.desc())
    )
    return db.scalars(stmt).all()


@router.get("/{purchase_id}", response_model=PurchaseOut)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    purchase = db.scalar(
        select(Purchase)
        .options(selectinload(Purchase.items))
        .where(Purchase.purchase_id == purchase_id)
    )
    if purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase


@router.post("/", response_model=PurchaseOut, status_code=status.HTTP_201_CREATED)
def create_purchase(
    body: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_buy),
):
    """Stock in: insert purchase + lines, then increase product.stock_quantity.
    If anything fails, the whole transaction rolls back."""
    if db.get(Supplier, body.supplier_id) is None:
        raise HTTPException(status_code=400, detail="Supplier not found")

    purchase = Purchase(
        supplier_id=body.supplier_id,
        created_by_user_id=current_user.user_id,
        status="Received",
        total_amount=Decimal("0"),
    )
    db.add(purchase)
    db.flush()  # get purchase_id before inserting items

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
        unit_cost = line.unit_cost if line.unit_cost is not None else product.cost_price
        db.add(
            PurchaseItem(
                purchase_id=purchase.purchase_id,
                product_id=product.product_id,
                quantity=line.quantity,
                unit_cost=unit_cost,
            )
        )
        product.stock_quantity += line.quantity
        total += unit_cost * line.quantity

    purchase.total_amount = total
    db.commit()
    db.refresh(purchase)
    db.refresh(purchase, attribute_names=["items"])
    return purchase
