from typing import Optional

from pydantic import BaseModel

from app.common.schemas import omit
from app.common.schemas.document import Document
from app.supplier.schemas.address import Address, AddressCreate


class SupplierBase(BaseModel):
    document: Document
    business_name: str
    address_id: int


class SupplierCreateId(SupplierBase):
    ...


@omit("address_id")
class SupplierCreate(SupplierBase):
    address: AddressCreate


class SupplierUpdate(BaseModel):
    business_name: Optional[str] = None
    document: Optional[Document] = None


class Supplier(BaseModel):
    id: int
    address: Address
