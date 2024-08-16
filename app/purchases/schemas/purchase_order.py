from datetime import date
from typing import List, Optional
from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import Enum

from app.purchases.schemas.purchase_order_item import (
    PurchaseOrderItem,
    PurchaseOrderItemCreateBody,
)
from app.supplier.schemas.supplier import Supplier


class PurchaseStatusEnum(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    RECEIVED = "RECEIVED"
    LOTTED = "LOTTED"


class PurchaseOrderBase(BaseModel):
    expected_arrival_date: date
    status: PurchaseStatusEnum


class PurchaseOrderCreate(PurchaseOrderBase):
    supplier_id: int
    items: List[PurchaseOrderItemCreateBody]


class PurchaseOrderUpdate(BaseModel):
    ...


class PurchaseOrder(PurchaseOrderBase):
    id: int
    supplier: Supplier
    items: List[PurchaseOrderItem]


class PurchaseOrderListParams(BaseModel):
    q: Optional[str] = Field(
        Query(None, description="Simple search by Supplier business name")
    )
    status: Optional[str] = Field(
        Query(None, description="Filter by Purchase Order status")
    )
    expected_arrival_date: Optional[date] = Field(
        Query(None, description="Filter by Purchase Order expected arrival date")
    )
