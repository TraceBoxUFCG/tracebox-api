from app.common.repositories.base import BaseRepository
from sqlalchemy.orm import Session

from app.stock.models.stock_transaction import StockTransactionModel


class StockTransactionRepository(
    BaseRepository[StockTransactionModel, int],
):
    def __init__(self, db: Session):
        super().__init__(
            StockTransactionModel.id, model_class=StockTransactionModel, db=db
        )
