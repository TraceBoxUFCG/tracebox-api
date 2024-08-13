from decimal import Decimal
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field

from app.catalog.schemas.packaging import Packaging, PackagingCreate


class ProductBase(BaseModel):
    name: str
    average_unit_weight: Decimal


class ProductCreate(ProductBase):
    packaging: PackagingCreate


class ProductCreateId(ProductBase):
    packaging_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    average_unit_weight: Optional[Decimal] = None


class Product(ProductBase):
    id: int
    packaging: Packaging


class ProductListParams(BaseModel):
    q: Optional[str] = Field(Query(None, description="Simple search by Product name"))
