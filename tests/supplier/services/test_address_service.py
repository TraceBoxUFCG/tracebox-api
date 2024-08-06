import pytest
from sqlalchemy.orm import Session

from app.common.schemas.states import StatesEnum
from app.supplier.schemas.address import AddressCreate
from app.supplier.services.address import AddressService


@pytest.fixture
def service(session: Session):
    return AddressService(db=session)


class TestAdressService:
    def test_create_address(self, service: AddressService):
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

        print(payload)

        response = service.create(payload)

        assert response.city == payload.city
        assert response.state == payload.state
        assert response.street == payload.street
        assert response.zipcode == payload.zipcode
        assert response.complement == payload.complement
        assert response.number == payload.number
        assert response.latitude == payload.latitude
        assert response.longitude == payload.longitude
