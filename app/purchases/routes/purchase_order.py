from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.purchases.deps import get_purchase_order_service
from app.purchases.schemas.purchase_order import (
    PurchaseOrder,
    PurchaseOrderCreateOrUpdate,
    PurchaseOrderListParams,
)
from app.purchases.services.purchase_order import PurchaseOrderService
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter()


@router.post("/place", response_model=PurchaseOrder)
def place(
    payload: PurchaseOrderCreateOrUpdate,
    service: PurchaseOrderService = Depends(get_purchase_order_service),
):
    return service.place(create_or_update=payload)


@router.get("/", response_model=Page[PurchaseOrder])
def get_all_purchase_order(
    params: PurchaseOrderListParams = Depends(),
    service: PurchaseOrderService = Depends(get_purchase_order_service),
):
    return paginate(service.get_all_for_pagination(params=params))


@router.get("/{id}", response_model=PurchaseOrder)
def get_purchase_order_by_id(
    id: int,
    service: PurchaseOrderService = Depends(get_purchase_order_service),
):
    return service.get_by_id(id=id)


@router.post("/{id}/confirm", response_model=PurchaseOrder)
def confirm_purchase_order(
    id: int,
    service: PurchaseOrderService = Depends(get_purchase_order_service),
):
    return service.confirm(id=id)
