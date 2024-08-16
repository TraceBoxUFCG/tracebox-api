from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.purchases.models.purchase_order_item import PurchaseOrderItemModel


class PurchaseOrdeItemRepository(
    BaseRepository[PurchaseOrderItemModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            PurchaseOrderItemModel.id,
            model_class=PurchaseOrderItemModel,
            db=db,
        )
