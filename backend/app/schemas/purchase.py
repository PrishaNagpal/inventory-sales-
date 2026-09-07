from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PurchaseItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_cost: Decimal | None = Field(default=None, ge=0)


class PurchaseCreate(BaseModel):
    supplier_id: int
    items: list[PurchaseItemIn] = Field(min_length=1)


class PurchaseItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    purchase_item_id: int
    product_id: int
    quantity: int
    unit_cost: Decimal


class PurchaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    purchase_id: int
    supplier_id: int
    created_by_user_id: int | None
    purchase_date: datetime
    total_amount: Decimal
    status: str
    items: list[PurchaseItemOut]
