from uuid import UUID

from sqlalchemy.orm import Session

from app.common.repositories.base import BaseFinder, BaseRepository
from app.supplier.models.supplier import SupplierModel


class SupplierFinder(BaseFinder[SupplierModel]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls(db.query(SupplierModel).filter(SupplierModel.deleted_at.is_(None)))

    def filtered_by_business_name_ilike(self, target: str):
        if target:
            return SupplierFinder(
                (
                    self.base_query.filter(
                        SupplierModel.business_name.ilike(f"%{target.strip()}%")
                    )
                )
            )
        return self

    def search_by_query_criterias(self, target: str):
        business_name_query = self.filtered_by_business_name_ilike(target=target).query

        return SupplierFinder(business_name_query)


class SupplierRepository(
    BaseRepository[SupplierModel, UUID],
):
    finder: SupplierFinder

    def __init__(self, db: Session):
        super().__init__(
            SupplierModel.id,
            model_class=SupplierModel,
            finder=SupplierFinder,
            db=db,
        )
