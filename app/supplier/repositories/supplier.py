from uuid import UUID

from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.supplier.models.supplier import SupplierModel


class SupplierRepository(
    BaseRepository[SupplierModel, UUID],
):
    def __init__(self, db: Session):
        super().__init__(
            SupplierModel.id,
            model_class=SupplierModel,
            db=db,
        )
