from app.common.services.base import BaseService
from app.stock.repositories.stock_transaction import StockTransactionRepository
from app.stock.schemas.stock_transaction import (
    StockTransaction,
    StockTransactionCreate,
    StockTransactionUpdate,
)
from sqlalchemy.orm import Session


class StockTransactionService(
    BaseService[StockTransactionCreate, StockTransactionUpdate, StockTransaction]
):
    db: Session
    repository: StockTransactionRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=StockTransactionRepository)
        self.db = db
