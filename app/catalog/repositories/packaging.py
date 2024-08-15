from sqlalchemy.orm import Session

from app.catalog.models.packaging import PackagingModel
from app.common.repositories.base import BaseRepository


class PackagingRepository(
    BaseRepository[PackagingModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            PackagingModel.id,
            model_class=PackagingModel,
            db=db,
        )
