from typing import List

from fastapi import HTTPException

from app.catalog.schemas.packaging import Packaging
from app.purchases.schemas.purchase_order import (
    PurchaseOrder,
    PurchaseOrderListParams,
    PurchaseOrderStatusEnum,
)
from app.purchases.services.purchase_order import PurchaseOrderService
from sqlalchemy.orm import Session

from app.receivement.schemas.asset_lot import AssetLot, AssetLotCreate, AssetLotUpdate
from app.receivement.schemas.lotting import LotReceivementItemPayload
from app.receivement.schemas.receivement_item import ReceivementItem
from app.receivement.services.asset_lot import AsseLotService
from app.receivement.services.receivement_item import ReceivementItemService
from app.stock.schemas.asset import AssetStatusEnum
from app.stock.services.asset import AssetService


class LottingService:
    db: Session

    def __init__(self, db: Session):
        self.db = db
        self.purchase_order_service = PurchaseOrderService(db=db)
        self.asset_lot_service = AsseLotService(db=db)
        self.receivement_item_service = ReceivementItemService(db=db)
        self.asset_service = AssetService(db=db)

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
        pending_lot = self.asset_lot_service.get_not_lotted_by_purchase_order_id(
            purchase_order_id=purchase_order_id
        )

        if pending_lot:
            raise HTTPException(
                status_code=400,
                detail="Cant finish lotting for purchase_order with pending items to lot",
            )

        return self.purchase_order_service.finish_lotting(id=purchase_order_id)

    def get_purchase_order(self, params: PurchaseOrderListParams):
        return self.purchase_order_service.get_all_for_pagination(params=params)

    def get_asset_lots(self, purchase_order_id: int) -> List[AssetLot]:
        return self.asset_lot_service.get_by_purchase_order_id(
            purchase_order_id=purchase_order_id
        )

    def lot_item(
        self, asset_lot_id: int, lotting_payload: LotReceivementItemPayload
    ) -> AssetLot:
        asset_id = lotting_payload.asset_id
        asset = self.asset_service.get_by_id(id=asset_id)

        asset_lot = self.asset_lot_service.get_by_id(id=asset_lot_id)
        receiment_item = asset_lot.receivement_item

        if asset_lot.asset_id:
            raise HTTPException(status_code=400, detail="Asset Lot already reviewd")

        if asset.status != AssetStatusEnum.EMPTY:
            raise HTTPException(status_code=400, detail="Cant use this asset to lot.")

        asset_lot = self.asset_lot_service.update(
            id=asset_lot_id, update=AssetLotUpdate(asset_id=asset_id)
        )
        packaging = self._get_receivement_item_packaging(
            receivement_item_id=receiment_item.id
        )
        self.asset_service.lot(id=asset_id, packaging=packaging)

        return asset_lot

    def _get_receivement_item_packaging(self, receivement_item_id: int) -> Packaging:
        receivement_item = self.receivement_item_service.get_by_id(
            id=receivement_item_id
        )

        return receivement_item.purchase_order_item.product_variety.product.packaging
