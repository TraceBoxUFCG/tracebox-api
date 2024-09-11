from typing import List
from app.common.repositories.base import BaseRepository

from sqlalchemy.orm import Session

from app.purchases.models.purchase_order_item import PurchaseOrderItemModel
from app.receivement.models.asset_lot import AssetLotModel
from app.receivement.models.receivement_item import ReceivementItemModel


class AssetLotRepository(
    BaseRepository[AssetLotModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            AssetLotModel.id,
            model_class=AssetLotModel,
            db=db,
        )

    def get_not_lotted_by_purchase_order_id(
        self, purchase_order_id: int
    ) -> List[AssetLotModel]:
        return (
            self.default_query.join(
                ReceivementItemModel,
                ReceivementItemModel.id == AssetLotModel.receivement_item_id,
            )
            .join(
                PurchaseOrderItemModel,
                ReceivementItemModel.purchase_order_item_id
                == PurchaseOrderItemModel.id,
            )
            .filter(PurchaseOrderItemModel.deleted_at.is_(None))
            .filter(ReceivementItemModel.deleted_at.is_(None))
            .filter(PurchaseOrderItemModel.purchase_order_id == purchase_order_id)
            .filter(AssetLotModel.asset_id.is_(None))
            .all()
        )

    def get_by_purchase_order_id(self, purchase_order_id: int) -> List[AssetLotModel]:
        return (
            self.default_query.join(
                ReceivementItemModel,
                ReceivementItemModel.id == AssetLotModel.receivement_item_id,
            )
            .join(
                PurchaseOrderItemModel,
                ReceivementItemModel.purchase_order_item_id
                == PurchaseOrderItemModel.id,
            )
            .filter(PurchaseOrderItemModel.deleted_at.is_(None))
            .filter(ReceivementItemModel.deleted_at.is_(None))
            .filter(PurchaseOrderItemModel.purchase_order_id == purchase_order_id)
            .all()
        )
