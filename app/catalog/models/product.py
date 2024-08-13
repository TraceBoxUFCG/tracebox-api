from sqlalchemy import Column, Index, Numeric, String, text
from app.common.database.database import Base
from app.common.models.table_model import TableModel


class ProductModel(Base, TableModel):
    __tablename__ = "product"
    __table_args__ = (
        Index(
            "ix_product_name_uniqueness",
            "name",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    name = Column(String, nullable=False)
    average_unit_weight = Column(Numeric, nullable=False)
