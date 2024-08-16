from app.common.services.base import BaseService
from app.purchases.repositories.purchase_order_item import PurchaseOrdeItemRepository
from app.purchases.schemas.purchase_order_item import (
    PurchaseOrderItem,
    PurchaseOrderItemCreate,
    PurchaseOrderItemUpdate,
)
from sqlalchemy.orm import Session


class PurchaseOrderItemService(
    BaseService[PurchaseOrderItemCreate, PurchaseOrderItemUpdate, PurchaseOrderItem]
):
    repository: PurchaseOrdeItemRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=PurchaseOrdeItemRepository)
