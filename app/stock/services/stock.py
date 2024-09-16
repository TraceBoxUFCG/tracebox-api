from typing import Optional
from app.common.exceptions import RecordNotFoundException
from app.common.services.base import BaseService
from app.stock.repositories.stock import StockFinder, StockRepository
from app.stock.schemas.stock import (
    Stock,
    StockCreate,
    StockDetail,
    StockListParams,
    StockUpdate,
)
from sqlalchemy.orm import Session

from app.stock.services.asset import AssetService
from app.stock.services.stock_transaction import StockTransactionService


class StockService(BaseService[StockCreate, StockUpdate, Stock]):
    db: Session
    repository: StockRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=StockRepository, return_model=Stock)
        self.db = db
        self.asset_service = AssetService(db=db)
        self.stock_transaction_service = StockTransactionService(db=db)

    def _get_all_query(self, params: StockListParams) -> StockFinder:
        filtered = self.repository.finder

        if params.q:
            filtered = filtered.search_by_query_criterias(target=params.q)

        return filtered

    def get_all_for_pagination(self, params: StockListParams):
        return self._get_all_query(params=params).query

    def get_by_product_id(self, product_id: int) -> Optional[Stock]:
        try:
            model = self.repository.get_by_product_id(product_id=product_id)
            return Stock.model_validate(model)
        except RecordNotFoundException:
            return None

    def get_stock_details(self, product_id: str) -> StockDetail:
        stock = self.get_by_product_id(product_id=product_id)
        transactions = self.stock_transaction_service.get_by_product_id(
            product_id=product_id
        )
        assets = self.asset_service.get_by_product_id(product_id=product_id)
        detail = StockDetail(stock=stock, transactions=transactions, assets=assets)
        return detail
