from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=150)
    contact_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = None


class SupplierUpdate(BaseModel):
    company_name: str | None = Field(default=None, min_length=1, max_length=150)
    contact_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = None


class SupplierOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    supplier_id: int
    company_name: str
    contact_name: str | None
    email: str | None
    phone: str | None
    address: str | None
    created_at: datetime
