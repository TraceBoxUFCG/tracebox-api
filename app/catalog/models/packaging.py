from sqlalchemy import Column, Computed, Enum, Numeric, String
from app.common.database.database import Base
from app.common.models.table_model import TableModel
from app.common.schemas.unit import UnitEnum


class PackagingModel(Base, TableModel):
    __tablename__ = "packaging"

    quantity = Column(Numeric, nullable=False)
    unit = Column(Enum(UnitEnum), nullable=False)
    description = Column(
        String,
        Computed("'PAC(' || quantity || enum_to_text(unit) || ')'"),
    )
