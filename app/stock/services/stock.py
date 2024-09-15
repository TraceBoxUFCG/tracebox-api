from typing import Optional
from app.common.exceptions import RecordNotFoundException
from app.common.services.base import BaseService
from app.stock.repositories.stock import StockFinder, StockRepository
from app.stock.schemas.stock import Stock, StockCreate, StockListParams, StockUpdate
from sqlalchemy.orm import Session


class StockService(BaseService[StockCreate, StockUpdate, Stock]):
    db: Session
    repository: StockRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=StockRepository)
        self.db = db

    def _get_all_query(self, params: StockListParams) -> StockFinder:
        filtered = self.repository.finder

        if params.q:
            filtered = filtered.search_by_query_criterias(target=params.q)

        return filtered

    def get_all_for_pagination(self, params: StockListParams):
        return self._get_all_query(params=params).query

    def get_by_product_id(self, product_id: int) -> Optional[Stock]:
        try:
            return self.repository.get_by_product_id(product_id=product_id)
        except RecordNotFoundException:
            return None
