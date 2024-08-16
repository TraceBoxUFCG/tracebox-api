from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.purchases.models.purchase_order import PurchaseOrderModel


class PurchaseOrderRepository(
    BaseRepository[PurchaseOrderModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            PurchaseOrderModel.id,
            model_class=PurchaseOrderModel,
            db=db,
        )
