from fastapi import APIRouter, Depends

from app.purchases.deps import get_purchase_order_service
from app.purchases.schemas.purchase_order import (
    PurchaseOrder,
    PurchaseOrderCreateOrUpdate,
)
from app.purchases.services.purchase_order import PurchaseOrderService


router = APIRouter()


@router.post("{purchase_order_id}/place", response_model=PurchaseOrder)
def place(
    payload: PurchaseOrderCreateOrUpdate,
    service: PurchaseOrderService = Depends(get_purchase_order_service),
):
    return service.place(create_or_update=payload)
