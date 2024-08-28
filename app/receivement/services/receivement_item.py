from app.common.services.base import BaseService

from app.receivement.repositories.receivement_item import ReceivementItemRepository

from sqlalchemy.orm import Session

from app.receivement.schemas.receivement_item import (
    ReceivementItem,
    ReceivementItemCreate,
    ReceivementItemUpdate,
)


class ReceivementItemService(
    BaseService[
        ReceivementItemCreate,
        ReceivementItemUpdate,
        ReceivementItem,
    ]
):
    db: Session
    repository: ReceivementItemRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=ReceivementItemRepository)
        self.db = db
