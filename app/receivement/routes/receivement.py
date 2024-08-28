from typing import List
from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.purchases.schemas.purchase_order import PurchaseOrder, PurchaseOrderListParams
from app.receivement.deps import get_receivement_service
from app.receivement.schemas.receivement import ReceiveItemPayload
from app.receivement.schemas.receivement_item import ReceivementItem
from app.receivement.services.receivement import ReceivementService
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter()


@router.get("/purchase_order", response_model=Page[PurchaseOrder])
def get_purchase_orders(
    params: PurchaseOrderListParams = Depends(),
    service: ReceivementService = Depends(get_receivement_service),
):
    return paginate(service.get_purchase_order(params=params))


@router.post(
    "/purchase_order/{purchase_order_id}/start", response_model=List[ReceivementItem]
)
def start(
    purchase_order_id: int,
    service: ReceivementService = Depends(get_receivement_service),
):
    return service.start(purchase_order_id=purchase_order_id)


@router.post("/purchase_order/{purchase_order_id}/finish", response_model=PurchaseOrder)
def finish(
    purchase_order_id: int,
    service: ReceivementService = Depends(get_receivement_service),
):
    return service.finish(purchase_order_id=purchase_order_id)


@router.get(
    "/purchase_order/{purchase_order_id}/receivement_item",
    response_model=List[ReceivementItem],
)
def get_receivement_items(
    purchase_order_id: int,
    service: ReceivementService = Depends(get_receivement_service),
):
    return service.get_receivement_items(purchase_order_id=purchase_order_id)


@router.post("/{receivement_item_id}/receive", response_model=ReceivementItem)
def receive_tem(
    receivement_item_id: int,
    receive_payload: ReceiveItemPayload,
    service: ReceivementService = Depends(get_receivement_service),
):
    return service.receive_item(
        receivement_item_id=receivement_item_id, receive_payload=receive_payload
    )
