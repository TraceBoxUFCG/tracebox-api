from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.supplier.repositories.supplier import SupplierRepository
from app.supplier.schemas.supplier import (
    Supplier,
    SupplierCreate,
    SupplierCreateId,
    SupplierUpdate,
)
from app.supplier.services.address import AddressService
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError


class SupplierService(BaseService[SupplierCreate, SupplierUpdate, Supplier]):
    db: Session
    repository: SupplierRepository
    address_service: AddressService

    def __init__(self, db: Session):
        self.address_service = AddressService(db=db)
        super().__init__(db=db, repository=SupplierRepository)
        self.db = db

    def create(self, create: SupplierCreate) -> Supplier:
        created_address = self.address_service.create(create=create.address)
        create = SupplierCreateId(
            address_id=created_address.id,
            document=create.document,
            business_name=create.business_name,
        )
        try:
            return self.repository.add(create_schema=create)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=409,
                    detail=f"Supplier with document {create.document} already exists",
                )
