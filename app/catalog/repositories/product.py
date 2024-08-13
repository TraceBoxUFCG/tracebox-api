from uuid import UUID

from sqlalchemy.orm import Session

from app.catalog.models.product import ProductModel
from app.common.repositories.base import BaseFinder, BaseRepository


class ProductFinder(BaseFinder[ProductModel]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls(db.query(ProductModel).filter(ProductModel.deleted_at.is_(None)))

    def filtered_by_name_ilike(self, target: str):
        if target:
            return ProductFinder(
                (self.base_query.filter(ProductModel.name.ilike(f"%{target.strip()}%")))
            )
        return self

    def search_by_query_criterias(self, target: str):
        name_query = self.filtered_by_name_ilike(target=target).query

        return ProductFinder(name_query)


class ProductRepository(
    BaseRepository[ProductModel, UUID],
):
    finder: ProductFinder

    def __init__(self, db: Session):
        super().__init__(
            ProductModel.id,
            model_class=ProductModel,
            finder=ProductFinder,
            db=db,
        )
