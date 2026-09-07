from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, computed_field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    sku: str = Field(min_length=1, max_length=50)
    description: str | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    cost_price: Decimal = Field(ge=0)
    selling_price: Decimal = Field(ge=0)
    low_stock_threshold: int = Field(default=10, ge=0)
    # stock_quantity is NOT here — stock changes via purchases/sales later


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    sku: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    cost_price: Decimal | None = Field(default=None, ge=0)
    selling_price: Decimal | None = Field(default=None, ge=0)
    low_stock_threshold: int | None = Field(default=None, ge=0)


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    category_id: int | None
    supplier_id: int | None
    name: str
    sku: str
    description: str | None
    cost_price: Decimal
    selling_price: Decimal
    stock_quantity: int
    low_stock_threshold: int
    created_at: datetime

    @computed_field
    @property
    def low_stock(self) -> bool:
        return self.stock_quantity <= self.low_stock_threshold
