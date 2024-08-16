from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field

from app.catalog.schemas.product import Product


class AssetStatusEnum(str, Enum):
    EMPTY = "EMPTY"
    OCCUPIED = "OCCUPIED"
    DISABLED = "DISABLED"


class AssetBase(BaseModel):
    status: AssetStatusEnum


class AssetCreate(BaseModel):
    packaging_id: Optional[int] = None


class AssetGeneratePayload(BaseModel):
    quantity: int


class AssetUpdate(BaseModel):
    status: Optional[AssetStatusEnum] = None
    packaging_id: Optional[int] = None


class Asset(AssetBase):
    id: int
    product: Optional[Product] = None


class AssetListParams(BaseModel):
    q: Optional[str] = Field(Query(None, description="Simple search by asset id"))


class SupplierListParams(BaseModel):
    q: Optional[str] = Field(
        Query(None, description="Simple search by Supplier business name")
    )
