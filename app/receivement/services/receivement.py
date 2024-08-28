from typing import List

from fastapi import HTTPException
from app.purchases.schemas.purchase_order import (
    PurchaseOrder,
    PurchaseOrderListParams,
    PurchaseOrderStatusEnum,
)
from app.purchases.services.purchase_order import PurchaseOrderService
from sqlalchemy.orm import Session

from app.receivement.schemas.receivement_item import (
    ReceivementItem,
    ReceivementItemCreate,
)
from app.receivement.services.receivement_item import (
    ReceivementItemService,
)


class ReceivementService:
    db: Session

    def __init__(self, db: Session):
        self.db = db
        self.purchase_order_service = PurchaseOrderService(db=db)
        self.receivement_item_service = ReceivementItemService(db=db)

    def start(self, purchase_order_id: int) -> List[ReceivementItem]:
        purchase_order: PurchaseOrder = self.purchase_order_service.get_by_id(
            id=purchase_order_id
        )

        if purchase_order.status != PurchaseOrderStatusEnum.CONFIRMED:
            raise HTTPException(
                status_code=409,
                detail=f"Cant start receivement for a purchase order with status {purchase_order.status.value}",
            )

        items = purchase_order.items

        receivements = []
        for item in items:
            payload = ReceivementItemCreate(
                purchase_order_item_id=item.id, received_quantity=0, rejected_quantity=0
            )
            receivement = self.receivement_item_service.create(create=payload)
            receivements.append(receivement)

        self.purchase_order_service.start_receivement(id=purchase_order_id)
        return receivements

    def finish(self, purchase_order_id: int):
        pending_receivements = (
            self.receivement_item_service.get_pending_by_purchase_order_id(
                purchase_order_id=purchase_order_id
            )
        )

        if pending_receivements:
            raise HTTPException(
                status_code=400,
                detail="Cant finish receivement for purchase_order with pending items to receive",
            )

        self.purchase_order_service.finish_receivement(
            purchase_order_id=purchase_order_id
        )

    def get_purchase_order(self, params: PurchaseOrderListParams):
        return self.purchase_order_service.get_all_for_pagination(params=params)

    def get_receivement_items(self, purchase_order_id: int) -> List[ReceivementItem]:
        return self.receivement_item_service.get_by_purchase_order_id(
            purchase_order_id=purchase_order_id
        )
