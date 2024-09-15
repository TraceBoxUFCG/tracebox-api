from app.catalog.models.packaging import PackagingModel
from app.catalog.models.product import ProductModel
from app.common.repositories.base import BaseRepository
from app.stock.models.stock import StockModel
from sqlalchemy.orm import Session


class StockRepository(
    BaseRepository[StockModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            StockModel.id,
            model_class=StockModel,
            db=db,
        )

    @property
    def default_query(self):
        return (
            super()
            .default_query.join(ProductModel, ProductModel.id == StockModel.product_id)
            .join(PackagingModel.id == StockModel.packaging_id)
            .filter(PackagingModel.deleted_at.is_(None))
            .filter(ProductModel.deleted_at.is_(None))
        )
