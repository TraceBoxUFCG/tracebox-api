from app.common.repositories.base import BaseRepository
from app.receivement.models.purchase_order_receivement import (
    PurchaseOrderReceivementModel,
)
from sqlalchemy.orm import Session


class PurchaseOrderReceivementRepository(
    BaseRepository[PurchaseOrderReceivementModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            PurchaseOrderReceivementModel.id,
            model_class=PurchaseOrderReceivementModel,
            db=db,
        )
