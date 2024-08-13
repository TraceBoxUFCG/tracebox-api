from decimal import Decimal

from pydantic import BaseModel

from app.common.schemas.unit import UnitEnum


class PackagingBase(BaseModel):
    quantity: Decimal
    unit: UnitEnum


class PackagingCreate(PackagingBase):
    ...


class PackagingUpdate(BaseModel):
    ...


class Packaging(PackagingBase):
    id: int
