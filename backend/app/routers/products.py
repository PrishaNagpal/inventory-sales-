from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.errors import commit_or_conflict
from app.models import Category, Product, Supplier, User
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate

router = APIRouter()
staff_write = require_roles("admin", "manager")


def _get_product_or_404(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def _validate_fks(db: Session, category_id: int | None, supplier_id: int | None) -> None:
    if category_id is not None and db.get(Category, category_id) is None:
        raise HTTPException(status_code=400, detail="Category not found")
    if supplier_id is not None and db.get(Supplier, supplier_id) is None:
        raise HTTPException(status_code=400, detail="Supplier not found")


@router.get("/", response_model=list[ProductOut])
def list_products(
    search: str | None = None,
    category_id: int | None = None,
    low_stock: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stmt = select(Product)
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(or_(Product.name.ilike(pattern), Product.sku.ilike(pattern)))
    if category_id is not None:
        stmt = stmt.where(Product.category_id == category_id)
    if low_stock:
        stmt = stmt.where(Product.stock_quantity <= Product.low_stock_threshold)
    return db.scalars(stmt.order_by(Product.name)).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return _get_product_or_404(db, product_id)


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    body: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(staff_write),
):
    _validate_fks(db, body.category_id, body.supplier_id)
    product = Product(**body.model_dump(), stock_quantity=0)
    db.add(product)
    commit_or_conflict(db, "SKU already exists")
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    body: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(staff_write),
):
    product = _get_product_or_404(db, product_id)
    data = body.model_dump(exclude_unset=True)
    _validate_fks(db, data.get("category_id"), data.get("supplier_id"))
    for field, value in data.items():
        setattr(product, field, value)
    commit_or_conflict(db, "SKU already exists")
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(staff_write),
):
    product = _get_product_or_404(db, product_id)
    db.delete(product)
    db.commit()
