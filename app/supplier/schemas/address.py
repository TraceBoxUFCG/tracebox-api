from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.common.schemas.states import StatesEnum


class AddressBase(BaseModel):
    city: Optional[str] = None
    state: Optional[StatesEnum] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    latitude: float
    longitude: float


class AddressCreate(AddressBase):
    ...


class AddressUpdate(AddressBase):
    city: Optional[str] = None
    state: Optional[StatesEnum] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AddressView(AddressBase):
    id: UUID

    class Config:
        orm_mode = True