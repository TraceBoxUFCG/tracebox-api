from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.purchases.schemas.purchase_order_item import PurchaseOrderItem


class ReceivementItemStatusEnum(str, Enum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"


class ReceivementItemBase(BaseModel):
    purchase_order_item_id: int
    status: ReceivementItemStatusEnum
    received_quantity: int
    rejected_quantity: int


class ReceivementItemCreate(BaseModel):
    purchase_order_item_id: int
    received_quantity: int
    rejected_quantity: int


class ReceivementItem(ReceivementItemBase):
    id: int
    purchase_order_item: PurchaseOrderItem


class ReceivementItemUpdate(BaseModel):
    received_quantity: Optional[int] = None
    rejected_quantity: Optional[int] = None
    status: Optional[ReceivementItemStatusEnum] = None
