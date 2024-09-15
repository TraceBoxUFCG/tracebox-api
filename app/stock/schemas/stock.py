from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field

from app.catalog.schemas.product import Product


class StockBase(BaseModel):
    quantity: int
    product_id: int


class StockCreate(StockBase):
    ...


class StockUpdate(StockBase):
    quantity: Optional[int]


class Stock(StockBase):
    product: Product


class StockListParams(BaseModel):
    q: Optional[str] = Field(Query(None, description="Simple search by product name"))
