from app.common.repositories.base import BaseRepository
from app.receivement.models.receivement_item import (
    ReceivementItemModel,
)
from sqlalchemy.orm import Session


class ReceivementItemRepository(
    BaseRepository[ReceivementItemModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            ReceivementItemModel.id,
            model_class=ReceivementItemModel,
            db=db,
        )
