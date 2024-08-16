from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.catalog.schemas.product_variety import ProductVariety


class PurchaseOrderItemBase(BaseModel):
    boxes_quantity: int
    unit_price: Decimal


class PurchaseOrderItemCreateOrUpdate(PurchaseOrderItemBase):
    id: Optional[int] = None
    product_variety_id: int
    purchase_order_id: int


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    purchase_order_id: int
    product_variety_id: int


class PurchaseOrderItemUpdate(BaseModel):
    boxes_quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None


class PurchaseOrderItem(PurchaseOrderItemBase):
    id: int
    product_variety: ProductVariety
