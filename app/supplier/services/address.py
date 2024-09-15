from sqlalchemy.orm import Session

from app.common.client.google import GoogleClient
from app.common.services.base import BaseService
from app.supplier.repositories.address import AddressRepository
from app.supplier.schemas.address import AddressCreate, AddressUpdate, Address


class AddressService(BaseService[AddressCreate, AddressUpdate, Address]):
    db: Session
    repository: AddressRepository
    google_client: GoogleClient

    def __init__(self, db: Session):
        super().__init__(db=db, repository=AddressRepository, return_model=Address)
        self.db = db
        self.google_client = GoogleClient()

    def create(self, create: AddressCreate) -> Address:
        if create.latitude and create.longitude:
            return super().create(create)
        else:
            address = f"{create.city} {create.state} {create.city} {create.zipcode} {create.number}"
            latitude, longitude = self.google_client.get_location_coordinates(address)
            create.latitude = latitude
            create.longitude = longitude

            return super().create(create)
