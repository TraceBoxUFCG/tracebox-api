from pydantic import BaseModel

from app.common.schemas.unit import UnitEnum


class PackagingBase(BaseModel):
    quantity: float
    unit: UnitEnum


class PackagingCreate(PackagingBase):
    ...


class PackagingUpdate(BaseModel):
    ...


class Packaging(PackagingBase):
    id: int
    description: str
