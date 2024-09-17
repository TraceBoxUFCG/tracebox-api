from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, Field

from app.catalog.schemas.product import Product
from app.stock.schemas.asset import Asset
from app.stock.schemas.stock_transaction import StockTransaction


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


class Packaging(BaseModel):
    description: str

    model_config = {"from_attributes": True}


class StockDetail(BaseModel):
    stock: Stock
    transactions: List[StockTransaction]
    assets: List[Asset]
