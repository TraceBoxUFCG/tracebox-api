from fastapi import HTTPException
import pytest
from sqlalchemy.orm import Session

from app.common.schemas.states import StatesEnum
from app.supplier.models.supplier import SupplierModel
from app.supplier.schemas.address import AddressCreate
from app.supplier.schemas.supplier import SupplierCreate, SupplierUpdate
from app.supplier.services.supplier import SupplierService


@pytest.fixture
def service(session: Session):
    return SupplierService(db=session)


class TestSupplierService:
    @pytest.fixture
    def setup(self, make_supplier, session):
        self.supplier: SupplierModel = make_supplier()

        session.add(self.supplier)
        session.commit()

    def test_should_create_supplier_with_cpf(self, service: SupplierService):
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

    def test_should_create_supplier_with_cnpj(self, service: SupplierService):
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
            document="29444285000131",
            business_name="Antonio Bertino de Vasconcelos Cabral Neto",
            address=address,
        )

        response = service.create(payload)

        assert response.document == payload.document

    def test_should_update_supplier(self, setup, service: SupplierService):
        payload = SupplierUpdate(business_name="new business_name")

        response = service.update(id=self.supplier.id, update=payload)

        assert payload.business_name == response.business_name

    def test_should_raise_when_invalid_document_on_create(self):
        with pytest.raises(ValueError):
            SupplierCreate(document="111111111")

    def test_should_raise_when_invalid_document_on_update(self):
        with pytest.raises(ValueError):
            SupplierUpdate(document="111111111")

    def test_should_raise_when_creating_supplier_with_same_document(
        self, setup, service: SupplierService
    ):
        with pytest.raises(HTTPException):
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
                document=self.supplier.document,
                business_name="Antonio Bertino de Vasconcelos Cabral Neto",
                address=address,
            )

            service.create(payload)
