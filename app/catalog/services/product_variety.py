import csv
from io import StringIO
from typing import List
from fastapi import HTTPException
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.catalog.repositories.product_variety import (
    ProductVarietyFinder,
    ProductVarietyRepository,
)
from app.catalog.schemas.product_variety import (
    ProductVariety,
    ProductVarietyCreate,
    ProductVarietyListParams,
    ProductVarietyUpdate,
)
from app.common.services.base import BaseService
from fastapi import UploadFile


class ProductVarietyService(
    BaseService[ProductVarietyCreate, ProductVarietyUpdate, ProductVariety]
):
    db: Session
    repository: ProductVarietyRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=ProductVarietyRepository)
        self.db = db

    def create(self, create: ProductVarietyCreate) -> ProductVariety:
        try:
            return self.repository.add(create_schema=create)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=409,
                    detail=f"Product Variety with name {create.name} already exists",
                )

    async def import_from_csv(self, file: UploadFile):
        product_varieties = await self._parse_csv_file_to_product_variety_create(
            file=file
        )

        created_varieties = [
            self.create(create=product_variety) for product_variety in product_varieties
        ]

        return created_varieties

    async def _parse_csv_file_to_product_variety_create(
        self, file: UploadFile
    ) -> List[ProductVarietyCreate]:
        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=400, detail="Invalid file format. Please upload a CSV file."
            )

        contents = await file.read()
        decoded_content = contents.decode("utf-8")
        reader = csv.DictReader(StringIO(decoded_content))

        product_varieties = []

        for row in reader:
            product_variety = ProductVarietyCreate(
                product_id=int(row["product_id"]), name=row["name"]
            )
            product_varieties.append(product_variety)

        return product_varieties

    def _get_all_query(self, params: ProductVarietyListParams) -> ProductVarietyFinder:
        filtered = self.repository.finder

        if params.q:
            filtered = filtered.search_by_query_criterias(target=params.q)

        return filtered

    def get_all_for_pagination(self, params: ProductVarietyListParams):
        return self._get_all_query(params=params).query
