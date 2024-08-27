from datetime import date
from enum import Enum
from typing import List, Optional
from fastapi import Query
from pydantic import BaseModel, Field

from app.purchases.schemas.purchase_order_item import (
    PurchaseOrderItem,
    PurchaseOrderItemCreateOrUpdate,
)
from app.supplier.schemas.supplier import Supplier


class PurchaseOrderStatusEnum(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    RECEIVED = "RECEIVED"
    LOTTED = "LOTTED"


class PurchaseOrderBase(BaseModel):
    expected_arrival_date: date
    status: PurchaseOrderStatusEnum


class PurchaseOrderCreate(BaseModel):
    expected_arrival_date: date
    supplier_id: int


class PurchaseOrderCreateOrUpdate(BaseModel):
    id: Optional[int] = None
    expected_arrival_date: date
    supplier_id: int
    items: List[PurchaseOrderItemCreateOrUpdate]


class PurchaseOrderUpdate(BaseModel):
    expected_arrival_date: Optional[date] = None
    status: Optional[PurchaseOrderStatusEnum] = None


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
