from typing import Optional

from pydantic import BaseModel

from app.common.schemas.document import Document
from app.supplier.schemas.address import Address, AddressCreate


class SupplierBase(BaseModel):
    document: Document
    business_name: str


class SupplierCreateId(SupplierBase):
    address_id: int


class SupplierCreate(SupplierBase):
    address: AddressCreate


class SupplierUpdate(BaseModel):
    business_name: Optional[str] = None
    document: Optional[Document] = None


class Supplier(SupplierBase):
    id: int
    address: Address
