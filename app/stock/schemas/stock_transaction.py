from enum import Enum
from pydantic import BaseModel
from app.catalog.schemas.packaging import Packaging
from app.catalog.schemas.product import Product


class StockTransactionTypeEnum(str, Enum):
    ENTRY = "ENTRY"
    OUT = "OUT"


class StockTransactionBase(BaseModel):
    quantity: int
    product_id: int
    packaging_id: int
    type: StockTransactionTypeEnum
    meta: dict


class StockTransactionCreate(StockTransactionBase):
    ...


class StockTransactionUpdate(StockTransactionBase):
    ...


class StockTransaction(StockTransactionBase):
    product: Product
    packaging: Packaging
