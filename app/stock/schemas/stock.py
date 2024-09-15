from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field

from app.catalog.schemas.product import Product


class StockBase(BaseModel):
    quantity: int
    product_id: int


class StockCreate(StockBase):
    ...


class StockUpdate(BaseModel):
    quantity: Optional[int]


class Stock(StockBase):
    id: int
    product: Product

    model_config = {"from_attributes": True}


class StockListParams(BaseModel):
    q: Optional[str] = Field(Query(None, description="Simple search by product name"))


class Asset(BaseModel):
    id: int

    model_config = {"from_attributes": True}


class StockDetail(BaseModel):
    stock: Stock
