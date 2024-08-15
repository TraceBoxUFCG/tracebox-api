from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field

from app.catalog.schemas.product import Product


class ProductVarietyBase(BaseModel):
    name: str


class ProductVarietyCreate(ProductVarietyBase):
    id_product: int


class ProductVarietyUpdate(BaseModel):
    ...


class ProductVariety(ProductVarietyBase):
    id: int
    product: Product


class ProductVarietyListParams(BaseModel):
    q: Optional[str] = Field(
        Query(None, description="Simple search by product variety name")
    )