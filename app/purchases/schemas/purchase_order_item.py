from decimal import Decimal

from pydantic import BaseModel

from app.catalog.schemas.product_variety import ProductVariety


class PurchaseOrderItemBase(BaseModel):
    boxes_quantity: int
    unit_price: Decimal


class PurchaseOrderItemCreateBody(PurchaseOrderItemBase):
    product_variety_id: int


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    purchase_order_id: int
    product_variety_id: int


class PurchaseOrderItemUpdate(BaseModel):
    ...


class PurchaseOrderItem(PurchaseOrderItemBase):
    id: int
    product_variety: ProductVariety
