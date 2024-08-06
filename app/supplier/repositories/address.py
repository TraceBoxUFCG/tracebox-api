from uuid import UUID

from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.supplier.models.address import AddressModel


class AddressRepository(
    BaseRepository[AddressModel, UUID],
):
    def __init__(self, db: Session):
        super().__init__(
            AddressModel.id,
            model_class=AddressModel,
            db=db,
        )
