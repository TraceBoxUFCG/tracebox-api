from sqlalchemy.orm import Session

from app.catalog.models.product_variety import ProductVarietyModel
from app.common.repositories.base import BaseFinder, BaseRepository


class ProductVarietyFinder(BaseFinder[ProductVarietyModel]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls(
            db.query(ProductVarietyModel).filter(
                ProductVarietyModel.deleted_at.is_(None)
            )
        )

    def filtered_by_name_ilike(self, target: str):
        if target:
            return ProductVarietyFinder(
                (
                    self.base_query.filter(
                        ProductVarietyModel.name.ilike(f"%{target.strip()}%")
                    )
                )
            )
        return self

    def search_by_query_criterias(self, target: str):
        name_query = self.filtered_by_name_ilike(target=target).query

        return ProductVarietyFinder(name_query)


class ProductVarietyRepository(
    BaseRepository[ProductVarietyModel, int],
):
    finder: ProductVarietyFinder

    def __init__(self, db: Session):
        super().__init__(
            ProductVarietyModel.id,
            model_class=ProductVarietyModel,
            finder=ProductVarietyFinder,
            db=db,
        )
