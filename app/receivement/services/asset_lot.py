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
        super().__init__(db=db, repository=AssetLotRepository)
        self.db = db
