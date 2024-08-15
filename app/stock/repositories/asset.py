from uuid import UUID

from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.stock.models.asset import AssetModel


class AssetRepository(
    BaseRepository[AssetModel, UUID],
):
    def __init__(self, db: Session):
        super().__init__(
            AssetModel.id,
            model_class=AssetModel,
            db=db,
        )
