from fastapi import HTTPException
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
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

    def create(self, create: ReceivementItemCreate) -> ReceivementItem:
        try:
            return super().create(create)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=409,
                    detail=f"Receivement item for purchase_order item {create.purchase_order_item_id} already exists",
                )
