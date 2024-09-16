from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.catalog.repositories.product import ProductFinder, ProductRepository
from app.catalog.schemas.product import (
    Product,
    ProductCreate,
    ProductCreateId,
    ProductListParams,
    ProductUpdate,
)
from app.catalog.services.packaging import PackagingService
from app.common.services.base import BaseService
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError


class ProductService(BaseService[ProductCreate, ProductUpdate, Product]):
    db: Session
    repository: ProductRepository
    packaging_service: PackagingService

    def __init__(self, db: Session):
        super().__init__(db=db, repository=ProductRepository, return_model=Product)
        self.db = db
        self.packaging_service = PackagingService(db=db)

    def create(self, create: ProductCreate) -> Product:
        created_packaging = self.packaging_service.create(create=create.packaging)

        create = ProductCreateId(
            packaging_id=created_packaging.id,
            name=create.name,
            average_unit_weight=create.average_unit_weight,
        )
        try:
            return self.repository.add(create_schema=create)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=409,
                    detail=f"Product with name {create.name} already exists",
                )

    def _get_all_query(self, params: ProductListParams) -> ProductFinder:
        filtered = self.repository.finder

        if params.q:
            filtered = filtered.search_by_query_criterias(target=params.q)

        return filtered

    def get_all_for_pagination(self, params: ProductListParams):
        return self._get_all_query(params=params).query
