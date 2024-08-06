import pytest
from sqlalchemy.orm import Session

from app.common.exceptions import RecordNotFoundException
from app.common.schemas.states import StatesEnum
from app.supplier.schemas.address import AddressCreate, Address, AddressUpdate
from app.supplier.services.address import AddressService


@pytest.fixture
def service(session: Session):
    return AddressService(db=session)


@pytest.fixture
def address(service):
    payload: AddressCreate = AddressCreate(
        city="Campina Grande",
        state=StatesEnum.PB,
        street="Avenida Marechal Floriano Peixoto",
        zipcode="58434500",
        complement="Perto do Trauma",
        number="2132",
        latitude=0.23,
        longitude=0.23,
    )

    return service.create(payload)


class TestAdressService:
    def test_should_create_address(self, service: AddressService):
        payload: AddressCreate = AddressCreate(
            city="Campina Grande",
            state=StatesEnum.PB,
            street="Avenida Marechal Floriano Peixoto",
            zipcode="58434500",
            complement="Perto do Trauma",
            number="2132",
            latitude=0.23,
            longitude=0.23,
        )

        response = service.create(payload)

        assert response.city == payload.city
        assert response.state == payload.state
        assert response.street == payload.street
        assert response.zipcode == payload.zipcode
        assert response.complement == payload.complement
        assert response.number == payload.number
        assert response.latitude == payload.latitude
        assert response.longitude == payload.longitude

    def test_sould_raise_exception_when_not_valid_zipcode(self):
        with pytest.raises(ValueError):
            AddressCreate(
                city="Campina Grande",
                state=StatesEnum.PB,
                street="Avenida Marechal Floriano Peixoto",
                zipcode="584345000",
                complement="Perto do Trauma",
                number="2132",
                latitude=0.23,
                longitude=0.23,
            )

    def test_should_create_with_none_fields(self, service: AddressService):
        payload: AddressCreate = AddressCreate(
            city=None,
            state=None,
            street=None,
            zipcode=None,
            complement=None,
            number=None,
            latitude=0.23,
            longitude=0.23,
        )

        response = service.create(payload)

        assert response.city == payload.city
        assert response.state == payload.state
        assert response.street == payload.street
        assert response.zipcode == payload.zipcode
        assert response.complement == payload.complement
        assert response.number == payload.number
        assert response.latitude == payload.latitude
        assert response.longitude == payload.longitude

    def test_should_update(self, service: AddressService, address: Address):
        update_payload: AddressUpdate = AddressUpdate(city="New City")

        response = service.update(id=address.id, update=update_payload)

        assert response.city == update_payload.city

    def test_should_raise_when_invalid_zipcode(self):
        with pytest.raises(ValueError):
            AddressUpdate(zipcode="69432")

    def test_should_raise_when_updating_not_existing_address(
        self, service: AddressService
    ):
        with pytest.raises(RecordNotFoundException):
            update_payload: AddressUpdate = AddressUpdate(city="New City")
            service.update(id=9999, update=update_payload)

    def test_should_delete_address(self, service: AddressService, address: Address):
        assert service.delete(id=address.id) is True

    def test_should_raise_when_deleting_not_existing_address(
        self, service: AddressService
    ):
        with pytest.raises(RecordNotFoundException):
            service.delete(id=9999)
