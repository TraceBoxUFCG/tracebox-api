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
