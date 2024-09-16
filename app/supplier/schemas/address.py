from typing import Optional

from pydantic import BaseModel

from app.common.schemas.states import StatesEnum
from app.common.schemas.zipcode import ZipCode


class AddressBase(BaseModel):
    city: Optional[str] = None
    state: Optional[StatesEnum] = None
    street: Optional[str] = None
    zipcode: Optional[ZipCode] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AddressCreate(AddressBase):
    ...


class AddressUpdate(AddressBase):
    city: Optional[str] = None
    state: Optional[StatesEnum] = None
    street: Optional[str] = None
    zipcode: Optional[ZipCode] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Address(AddressBase):
    id: int

    model_config = {"from_attributes": True}
