from typing import Optional

from pydantic import BaseModel

from app.catalog.schemas.product_variety import ProductVariety
from app.supplier.schemas.supplier import Supplier


class PurchaseOrderItemBase(BaseModel):
    boxes_quantity: int
    unit_price: float


class PurchaseOrderItemCreateOrUpdate(PurchaseOrderItemBase):
    id: Optional[int] = None
    purchase_order_id: Optional[int] = None
    product_variety_id: int


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    purchase_order_id: int
    product_variety_id: int


class PurchaseOrderItemUpdate(BaseModel):
    boxes_quantity: Optional[int] = None
    unit_price: Optional[float] = None


class Receivement(BaseModel):
    status: str
    received_quantity: int
    rejected_quantity: int

    model_config = {"from_attributes": True}


class PurchaseOrder(BaseModel):
    supplier: Supplier

    model_config = {"from_attributes": True}


class PurchaseOrderItem(PurchaseOrderItemBase):
    id: int
    product_variety: ProductVariety
    receivement: Optional[Receivement] = None
    purchase_order: PurchaseOrder

    model_config = {"from_attributes": True}
