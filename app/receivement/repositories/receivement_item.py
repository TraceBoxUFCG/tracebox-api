from app.common.repositories.base import BaseRepository
from app.purchases.models.purchase_order_item import PurchaseOrderItemModel
from app.receivement.models.receivement_item import (
    ReceivementItemModel,
)
from sqlalchemy.orm import Session


class ReceivementItemRepository(
    BaseRepository[ReceivementItemModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            ReceivementItemModel.id,
            model_class=ReceivementItemModel,
            db=db,
        )

    def get_by_purchase_order_id(self, purchase_order_id: int):
        return (
            self.default_query.join(
                PurchaseOrderItemModel,
                ReceivementItemModel.purchase_order_item_id
                == PurchaseOrderItemModel.id,
            )
            .filter(PurchaseOrderItemModel.deleted_at.is_(None))
            .filter(PurchaseOrderItemModel.purchase_order_id == purchase_order_id)
            .all()
        )
