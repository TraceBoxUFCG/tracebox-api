from app.catalog.models.product import ProductModel
from app.common.exceptions import RecordNotFoundException
from app.common.repositories.base import BaseFinder, BaseRepository
from app.stock.models.stock import StockModel
from sqlalchemy.orm import Session


class StockFinder(BaseFinder[StockModel]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls(
            db.query(StockModel)
            .join(ProductModel, ProductModel.id == StockModel.product_id)
            .filter(
                StockModel.deleted_at.is_(None).filter(
                    ProductModel.deleted_at.is_(None)
                )
            )
        )

    def filtered_by_product_name(self, target: str):
        if target:
            return StockFinder(
                (self.base_query.filter(ProductModel.name.ilike(f"%{target.strip()}%")))
            )
        return self

    def search_by_query_criterias(self, target: str):
        product_name_query = self.filtered_by_product_name(target=target).query

        return StockFinder(product_name_query)


class StockRepository(
    BaseRepository[StockModel, int],
):
    finder: StockFinder

    def __init__(self, db: Session):
        super().__init__(
            StockModel.id, model_class=StockModel, db=db, finder=StockFinder
        )

    def get_by_product_id(self, product_id: int) -> StockModel:
        model = (
            self.db.query(StockModel)
            .filter(StockModel.product_id == product_id)
            .filter(StockModel.deleted_at.is_(None))
        )
        if not model:
            raise RecordNotFoundException()
        return model
