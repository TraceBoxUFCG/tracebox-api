from typing import List
from app.common.services.base import BaseService
from app.receivement.repositories.asset_lot import AssetLotRepository
from app.receivement.schemas.asset_lot import AssetLot, AssetLotCreate, AssetLotUpdate
from sqlalchemy.orm import Session


class AsseLotService(
    BaseService[
        AssetLotCreate,
        AssetLotUpdate,
        AssetLot,
    ]
):
    db: Session
    repository: AssetLotRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=AssetLotRepository, return_model=AssetLot)
        self.db = db

    def get_not_lotted_by_purchase_order_id(
        self, purchase_order_id: int
    ) -> List[AssetLot]:
        return self.repository.get_not_lotted_by_purchase_order_id(
            purchase_order_id=purchase_order_id
        )

    def get_by_purchase_order_id(self, purchase_order_id: int) -> List[AssetLot]:
        return self.repository.get_by_purchase_order_id(
            purchase_order_id=purchase_order_id
        )
