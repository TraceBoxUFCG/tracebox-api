from decimal import Decimal
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    average_unit_weight: Decimal


class ProductCreate(ProductBase):
    ...


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    average_unit_weight: Optional[Decimal] = None


class Product(ProductBase):
    id: int


class ProductListParams(BaseModel):
    q: Optional[str] = Field(Query(None, description="Simple search by Product name"))
