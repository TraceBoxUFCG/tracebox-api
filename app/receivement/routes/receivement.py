from typing import List
from fastapi import APIRouter, Depends

from app.receivement.deps import get_receivement_service
from app.receivement.schemas.receivement_item import ReceivementItem
from app.receivement.services.receivement import ReceivementService


router = APIRouter()


@router.post("{purchase_order_id}/start", response_model=List[ReceivementItem])
def start(
    purchase_order_id: int,
    service: ReceivementService = Depends(get_receivement_service),
):
    return service.start(purchase_order_id=purchase_order_id)
