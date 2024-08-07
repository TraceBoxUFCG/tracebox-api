from unittest import mock
import pytest

from app.supplier.models.supplier import SupplierModel
from tests.base_client import BaseClient


class SupplierClient(BaseClient):
    def __init__(self, client):
        super().__init__(client, endpoint_path="supplier")


@pytest.fixture
def client(client):
    return SupplierClient(client)


class TestSupplierService:
    @pytest.fixture
    def setup(self, make_supplier, session):
        self.supplier: SupplierModel = make_supplier()

        session.add(self.supplier)
        session.commit()

    def test_should_create_supplier_with_cpf(self, client: SupplierClient):
        payload = {
            "document": "12395321486",
            "business_name": "Business Name",
            "address": {
                "city": "Campina Grande",
                "state": "PB",
                "street": "Avenida Marechal Floriano Peixoto",
                "zipcode": "58534500",
                "number": "5255",
                "complement": "B06",
                "latitude": -1,
                "longitude": -2,
            },
        }

        response = client.create(payload)
        data = response.json()

        assert response.status_code == 200
        assert data["document"] == payload["document"]

    def test_should_create_supplier_with_cnpj(self, client: SupplierClient):
        payload = {
            "document": "29444285000131",
            "business_name": "Business Name",
            "address": {
                "city": "Campina Grande",
                "state": "PB",
                "street": "Avenida Marechal Floriano Peixoto",
                "zipcode": "58534500",
                "number": "5255",
                "complement": "B06",
                "latitude": -1,
                "longitude": -2,
            },
        }

        response = client.create(payload)
        data = response.json()

        assert response.status_code == 200
        assert data["document"] == payload["document"]

    def test_should_raise_when_invalid_document(self, client: SupplierClient):
        payload = {
            "document": "12134",
            "business_name": "Business Name",
            "address": {
                "city": "Campina Grande",
                "state": "PB",
                "street": "Avenida Marechal Floriano Peixoto",
                "zipcode": "58534500",
                "number": "5255",
                "complement": "B06",
                "latitude": -1,
                "longitude": -2,
            },
        }

        response = client.create(payload)

        assert response.status_code != 200

    def test_should_raise_when_creating_supplier_with_same_document(
        self, setup, client: SupplierClient
    ):
        supplier_doc = self.supplier.document
        payload = {
            "document": supplier_doc,
            "business_name": "Business Name",
            "address": {
                "city": "Campina Grande",
                "state": "PB",
                "street": "Avenida Marechal Floriano Peixoto",
                "zipcode": "58534500",
                "number": "5255",
                "complement": "B06",
                "latitude": -1,
                "longitude": -2,
            },
        }

        response = client.create(payload)
        data = response.json()

        assert response.status_code != 200
        assert data["detail"] == f"Supplier with document {supplier_doc} already exists"

    def test_should_create_with_coordinates_on_address(self, client: SupplierClient):
        payload = {
            "document": "29444285000131",
            "business_name": "Business Name",
            "address": {
                "city": "Campina Grande",
                "state": "PB",
                "street": "Avenida Marechal Floriano Peixoto",
                "zipcode": "58534500",
                "number": "5255",
                "complement": "B06",
                "latitude": -1,
                "longitude": -2,
            },
        }

        response = client.create(payload)
        data = response.json()

        assert response.status_code == 200
        assert data["address"]["latitude"] == payload["address"]["latitude"]
        assert data["address"]["longitude"] == payload["address"]["longitude"]

    def test_should_create_without_coordinates_on_address(self, client: SupplierClient):
        latitude = 2
        longitude = 3

        coordinates = (latitude, longitude)
        with mock.patch(
            "app.common.client.google.GoogleClient.get_location_coordinates",
            return_value=coordinates,
        ):
            payload = {
                "document": "29444285000131",
                "business_name": "Business Name",
                "address": {
                    "city": "Campina Grande",
                    "state": "PB",
                    "street": "Avenida Marechal Floriano Peixoto",
                    "zipcode": "58534500",
                    "number": "5255",
                    "complement": "B06",
                },
            }

            response = client.create(payload)
            data = response.json()

            assert response.status_code == 200
            assert data["address"]["latitude"] == latitude
            assert data["address"]["longitude"] == longitude

    def test_should_raise_when_invalid_zipcode(self, client: SupplierClient):
        payload = {
            "document": "29444285000131",
            "business_name": "Business Name",
            "address": {
                "city": "Campina Grande",
                "state": "PB",
                "street": "Avenida Marechal Floriano Peixoto",
                "zipcode": "2929292992",
                "number": "5255",
                "complement": "B06",
                "latitude": -1,
                "longitude": -2,
            },
        }

        response = client.create(payload)
        assert response.status_code != 200

    def test_should_return_supplier_by_id(self, setup, client: SupplierClient):
        response = client.get_by_id(id=self.supplier.id)
        supplier = response.json()

        assert response.status_code == 200
        assert supplier["id"] == self.supplier.id

    def test_should_raise_when_dont_find_supplier(self, client: SupplierClient):
        response = client.get_by_id(id=20)
        data = response.json()

        assert response.status_code != 200
        assert data["detail"] == "Entity not found"
