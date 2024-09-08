from typing import List

from app.purchases.schemas.purchase_order import (
    PurchaseOrder,
    PurchaseOrderListParams,
)
from app.purchases.services.purchase_order import PurchaseOrderService
from sqlalchemy.orm import Session

from app.receivement.schemas.asset_lot import AssetLot
from app.receivement.schemas.lotting import LotReceivementItemPayload
from app.receivement.services.asset_lot import AsseLotService


class LottingService:
    db: Session

    def __init__(self, db: Session):
        self.db = db
        self.purchase_order_service = PurchaseOrderService(db=db)
        self.asset_lot_service = AsseLotService(db=db)

    def start(self, purchase_order_id: int) -> List[AssetLot]:
        ...

    def finish(self, purchase_order_id: int) -> PurchaseOrder:
        ...

    def get_purchase_order(self, params: PurchaseOrderListParams):
        ...

    def get_asset_lots(self, purchase_order_id: int) -> List[AssetLot]:
        ...

    def lot_item(
        self, asset_lot_id: int, lotting_payload: LotReceivementItemPayload
    ) -> AssetLot:
        ...
