import pytest
from sqlalchemy.orm import Session

from app.common.schemas.states import StatesEnum
from app.supplier.schemas.address import AddressCreate
from app.supplier.schemas.supplier import SupplierCreate
from app.supplier.services.supplier import SupplierService


@pytest.fixture
def service(session: Session):
    return SupplierService(db=session)


class TestSupplierService:
    def test_should_create_supplier(self, service: SupplierService):
        address: AddressCreate = AddressCreate(
            city="Campina Grande",
            state=StatesEnum.PB,
            street="Avenida Marechal Floriano Peixoto",
            zipcode="58434500",
            complement="Perto do Trauma",
            number="2132",
            latitude=0.23,
            longitude=0.23,
        )

        payload: SupplierCreate = SupplierCreate(
            document="12395321486",
            business_name="Antonio Bertino de Vasconcelos Cabral Neto",
            address=address,
        )

        response = service.create(payload)

        assert response.document == payload.document
