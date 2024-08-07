from typing import Optional
import pytest

from app.common.schemas.states import StatesEnum
from app.supplier.models.address import AddressModel
from app.supplier.models.supplier import SupplierModel


@pytest.fixture
def make_address():
    defaults = dict(
        city="Campina Grande",
        state=StatesEnum.PB,
        street="Avenida Marechal Floriano Peixoto",
        zipcode="58434500",
        number="5255",
        complement="B06",
        latitude=-7.242622374339028,
        longitude=-35.935730207937425,
    )

    def _make_address(**overrides):
        return AddressModel(
            **{**defaults, **overrides},
        )

    return _make_address


@pytest.fixture
def make_supplier(make_address):
    defaults = dict(document="12395321486", business_name="Antonio Bertino")

    def _make_supplier(address: Optional[AddressModel] = None, **overrides):
        if not address:
            address = make_address()

        return SupplierModel(address=address, **{**defaults, **overrides})

    return _make_supplier
