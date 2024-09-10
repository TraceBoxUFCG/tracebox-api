from typing import List

from fastapi import HTTPException

from app.purchases.schemas.purchase_order import (
    PurchaseOrder,
    PurchaseOrderListParams,
    PurchaseOrderStatusEnum,
)
from app.purchases.services.purchase_order import PurchaseOrderService
from sqlalchemy.orm import Session

from app.receivement.schemas.asset_lot import AssetLot, AssetLotCreate
from app.receivement.schemas.lotting import LotReceivementItemPayload
from app.receivement.schemas.receivement_item import ReceivementItem
from app.receivement.services.asset_lot import AsseLotService
from app.receivement.services.receivement_item import ReceivementItemService


class LottingService:
    db: Session

    def __init__(self, db: Session):
        self.db = db
        self.purchase_order_service = PurchaseOrderService(db=db)
        self.asset_lot_service = AsseLotService(db=db)
        self.receivement_item_service = ReceivementItemService(db=db)

    def start(self, purchase_order_id: int) -> List[AssetLot]:
        purchase_order: PurchaseOrder = self.purchase_order_service.get_by_id(
            id=purchase_order_id
        )
        if purchase_order.status != PurchaseOrderStatusEnum.RECEIVED:
            raise HTTPException(
                status_code=409,
                detail=f"Cant start lotting for a purchase order with status {purchase_order.status.value}",
            )
        receivement_item_list = self.receivement_item_service.get_by_purchase_order_id(
            purchase_order_id=purchase_order_id
        )

        asset_lot_list = []
        for receivement_item in receivement_item_list:
            created_asset_lots = self._create_asset_lot_for_receivement_item(
                receivement_item=receivement_item
            )
            asset_lot_list.extend(created_asset_lots)

        self.purchase_order_service.start_lotting(id=purchase_order_id)

        return asset_lot_list

    def _create_asset_lot_for_receivement_item(
        self, receivement_item: ReceivementItem
    ) -> List[AssetLot]:
        received_crates = int(receivement_item.received_quantity)

        created_asset_lots = []
        for _ in range(received_crates):
            create_asset_lot_payload = AssetLotCreate(
                receivement_item_id=receivement_item.id
            )
            asset_lot = self.asset_lot_service.create(create=create_asset_lot_payload)
            created_asset_lots.append(asset_lot)

        return created_asset_lots

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
