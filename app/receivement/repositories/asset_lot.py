from app.common.repositories.base import BaseRepository

from sqlalchemy.orm import Session

from app.receivement.models.asset_lot import AssetLotModel


class AssetLotRepository(
    BaseRepository[AssetLotModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            AssetLotModel.id,
            model_class=AssetLotModel,
            db=db,
        )
