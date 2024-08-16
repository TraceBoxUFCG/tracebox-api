from typing import List
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
    db: Session

    def __init__(self, db: Session):
        super().__init__(db=db, repository=PurchaseOrdeItemRepository)
        self.db = db

    def place(
        self, purchase_order_id: int, items: List[PurchaseOrderItemCreateOrUpdate]
    ) -> PurchaseOrderItem:
        items_id = {item.id for item in items}
        current_items = self.get_items_by_purchase_order(
            purchase_order_id=purchase_order_id
        )
        items_to_delete = [item.id for item in current_items if item.id not in items_id]

        self.create_or_update(purchase_order_id=purchase_order_id, items=items)
        self.delete_items_in_batch(list_of_ids=items_to_delete)

        return self.get_items_by_purchase_order(purchase_order_id=purchase_order_id)

    def delete_items_in_batch(self, list_of_ids: List[int]):
        for id in list_of_ids:
            self.delete(id=id)

    def create_or_update(
        self, purchase_order_id: int, items: List[PurchaseOrderItemCreateOrUpdate]
    ):
        for item in items:
            existing_item = self.get_by_id(id=item.id) if item.id else None

            if existing_item:
                update_data = PurchaseOrderItemUpdate(
                    boxes_quantity=item.boxes_quantity,
                    unit_price=item.unit_price,
                )
                self.update(id=item.id, update=update_data)
            else:
                create_data = PurchaseOrderItemCreate(
                    boxes_quantity=item.boxes_quantity,
                    unit_price=item.unit_price,
                    product_variety_id=item.product_variety_id,
                    purchase_order_id=purchase_order_id,
                )
                self.create(create=create_data)

    def get_items_by_purchase_order(
        self, purchase_order_id: int
    ) -> List[PurchaseOrderItem]:
        return self.repository.get_by_purchase_order_id(
            purchase_order_id=purchase_order_id
        )
