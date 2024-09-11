from typing import List
from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.purchases.schemas.purchase_order import PurchaseOrder, PurchaseOrderListParams
from app.receivement.deps import get_lotting_service
from app.receivement.schemas.asset_lot import AssetLot
from fastapi_pagination.ext.sqlalchemy import paginate

from app.receivement.schemas.lotting import LotReceivementItemPayload
from app.receivement.services.lotting import LottingService


router = APIRouter()


@router.get("/purchase_order", response_model=Page[PurchaseOrder])
def get_purchase_orders(
    params: PurchaseOrderListParams = Depends(),
    service: LottingService = Depends(get_lotting_service),
):
    return paginate(service.get_purchase_order(params=params))


@router.post("/purchase_order/{purchase_order_id}/start", response_model=List[AssetLot])
def start(
    purchase_order_id: int,
    service: LottingService = Depends(get_lotting_service),
):
    return service.start(purchase_order_id=purchase_order_id)


@router.post("/purchase_order/{purchase_order_id}/finish", response_model=PurchaseOrder)
def finish(
    purchase_order_id: int,
    service: LottingService = Depends(get_lotting_service),
):
    return service.finish(purchase_order_id=purchase_order_id)


@router.get(
    "/purchase_order/{purchase_order_id}/asset_lot",
    response_model=List[AssetLot],
)
def get_asset_lots(
    purchase_order_id: int,
    service: LottingService = Depends(get_lotting_service),
):
    return service.get_asset_lots(purchase_order_id=purchase_order_id)


@router.post("/{asset_lot_id}/lot", response_model=AssetLot)
def lot_item(
    asset_lot_id: int,
    lotting_payload: LotReceivementItemPayload,
    service: LottingService = Depends(get_lotting_service),
):
    return service.lot_item(asset_lot_id=asset_lot_id, lotting_payload=lotting_payload)
