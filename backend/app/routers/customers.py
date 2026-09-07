from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.errors import commit_or_conflict
from app.models import Customer, User
from app.schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate

router = APIRouter()
staff_write = require_roles("admin", "manager", "cashier")


@router.get("/", response_model=list[CustomerOut])
def list_customers(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.scalars(
        select(Customer).order_by(Customer.last_name, Customer.first_name)
    ).all()


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(
    body: CustomerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(staff_write),
):
    data = body.model_dump()
    if data.get("email") is not None:
        data["email"] = str(data["email"])
    customer = Customer(**data)
    db.add(customer)
    commit_or_conflict(db, "Email already exists")
    db.refresh(customer)
    return customer


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(
    customer_id: int,
    body: CustomerUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(staff_write),
):
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    data = body.model_dump(exclude_unset=True)
    if data.get("email") is not None:
        data["email"] = str(data["email"])
    for field, value in data.items():
        setattr(customer, field, value)
    commit_or_conflict(db, "Email already exists")
    db.refresh(customer)
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "manager")),
):
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
