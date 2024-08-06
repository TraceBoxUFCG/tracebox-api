from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.supplier.repositories.address import AddressRepository
from app.supplier.schemas.address import AddressCreate, AddressUpdate, AddressView


class AddressService(BaseService[AddressCreate, AddressUpdate, AddressView]):
    db: Session
    repository: AddressRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=AddressRepository)
        self.db = db
