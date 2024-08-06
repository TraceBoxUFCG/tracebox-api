from sqlalchemy import Column
from app.common.database.database import Base
from app.common.models.table_model import TableModel
from sqlalchemy import String


class ProductModel(Base, TableModel):
    __tablename__ = "product"

    name = Column(String, nullable=False)

    document = Column(String, nullable=False)

    business_name = Column(String, nullable=False)
