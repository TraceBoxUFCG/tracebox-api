from typing import List

from fastapi import HTTPException
from app.purchases.schemas.purchase_order import PurchaseOrderStatusEnum
from app.purchases.services.purchase_order import PurchaseOrderService
from sqlalchemy.orm import Session

from app.purchases.services.purchase_order_item import PurchaseOrderItemService
from app.receivement.schemas.purchase_order_receivement import (
    PurchaseOrderReceivement,
    PurchaseOrderReceivementCreate,
)
from app.receivement.services.purchase_order_receivement import (
    PurchaseOrderReceivementService,
)


class ReceivementService:
    db: Session

    def __init__(self, db: Session):
        self.db = db
        self.purchase_order_service = PurchaseOrderService(db=db)
        self.purchase_order_item_service = PurchaseOrderItemService(db=db)
        self.purchase_order_receivement_service = PurchaseOrderReceivementService(db=db)

    def start(self, purchase_order_id: int) -> List[PurchaseOrderReceivement]:
        purchase_order = self.purchase_order_service.get_by_id(id=purchase_order_id)

        if purchase_order.status != PurchaseOrderStatusEnum.CONFIRMED:
            raise HTTPException(
                status_code=409,
                detail=f"Cant start receivement for a purchase order with status {purchase_order.status}",
            )

        items = self.purchase_order_item_service.get_all()

        receivements = []
        for item in items:
            payload = PurchaseOrderReceivementCreate(
                purchase_order_item_id=item.id, received_quantity=0, rejected_quantity=0
            )

            receivement = self.purchase_order_receivement_service.create(create=payload)
            receivements.append(receivement)

        return receivements
