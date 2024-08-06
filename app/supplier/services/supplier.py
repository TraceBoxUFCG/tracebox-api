from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.supplier.repositories.address import AddressRepository
from app.supplier.repositories.supplier import SupplierRepository
from app.supplier.schemas.supplier import (
    Supplier,
    SupplierCreate,
    SupplierCreateId,
    SupplierUpdate,
)
from app.supplier.services.address import AddressService


class SupplierService(BaseService[SupplierCreate, SupplierUpdate, Supplier]):
    db: Session
    repository: SupplierRepository
    address_service: AddressService

    def __init__(self, db: Session):
        self.address_service = AddressService(db=db)
        super().__init__(db=db, repository=AddressRepository)
        self.db = db

    def create(self, create: SupplierCreate) -> Supplier:
        created_address = self.address_service.create(create=create.address)

        create = SupplierCreateId(**create, address_id=created_address.id)
        supplier = self.repository.add(create_schema=create)
        return supplier
