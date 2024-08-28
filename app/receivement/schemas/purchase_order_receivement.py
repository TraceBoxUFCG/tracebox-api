from typing import Optional

from pydantic import BaseModel

from app.purchases.schemas.purchase_order_item import PurchaseOrderItem


class PurchaseOrderReceivementBase(BaseModel):
    purchase_order_item_id: int
    received_quantity: int
    rejected_quantity: int


class PurchaseOrderReceivementCreate(PurchaseOrderReceivementBase):
    ...


class PurchaseOrderReceivement(PurchaseOrderReceivementBase):
    purchase_order_item: PurchaseOrderItem


class PurchaseOrderReceivementUpdate(BaseModel):
    received_quantity: Optional[int] = None
    rejected_quantity: Optional[int] = None
