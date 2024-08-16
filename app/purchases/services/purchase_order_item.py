from app.common.services.base import BaseService
from app.purchases.repositories.purchase_order_item import PurchaseOrdeItemRepository
from app.purchases.schemas.purchase_order_item import (
    PurchaseOrderItem,
    PurchaseOrderItemCreate,
    PurchaseOrderItemCreateOrUpdate,
    PurchaseOrderItemUpdate,
)
from sqlalchemy.orm import Session


class PurchaseOrderItemService(
    BaseService[PurchaseOrderItemCreate, PurchaseOrderItemUpdate, PurchaseOrderItem]
):
    repository: PurchaseOrdeItemRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=PurchaseOrdeItemRepository)

    def place(
        self, purchase_order_id: int, create_or_update: PurchaseOrderItemCreateOrUpdate
    ) -> PurchaseOrderItem:
        existing_item = self.get_by_id(id=create_or_update.id)

        if existing_item:
            update_data = PurchaseOrderItemUpdate(
                boxes_quantity=create_or_update.boxes_quantity,
                unit_price=create_or_update.unit_price,
            )
            return self.update(id=create_or_update.id, update=update_data)
        else:
            create_data = PurchaseOrderItemCreate(
                boxes_quantity=create_or_update.boxes_quantity,
                unit_price=create_or_update.unit_price,
                product_variety_id=create_or_update.product_variety_id,
                purchase_order_id=create_or_update.purchase_order_id,
            )
            return self.create(create=create_data)
