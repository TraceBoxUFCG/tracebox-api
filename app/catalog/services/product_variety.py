from sqlalchemy.orm import Session

from app.catalog.repositories.product_variety import ProductVarietyRepository
from app.catalog.schemas.product_variety import (
    ProductVariety,
    ProductVarietyCreate,
    ProductVarietyUpdate,
)
from app.common.services.base import BaseService


class ProductVarietyService(
    BaseService[ProductVarietyCreate, ProductVarietyUpdate, ProductVariety]
):
    db: Session
    repository: ProductVarietyRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=ProductVarietyRepository)
        self.db = db
