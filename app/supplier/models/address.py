from sqlalchemy import Column, Float, String, Enum
from app.common.database.database import Base
from app.common.models.table_model import TableModel
from app.common.schemas.states import StatesEnum


class AddressModel(Base, TableModel):
    __tablename__ = "address"

    city = Column(String, nullable=True)
    state = Column(Enum(StatesEnum), nullable=True)
    number = Column(String, nullable=True)
    complement = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
