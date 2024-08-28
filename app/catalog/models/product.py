from sqlalchemy import Column, ForeignKey, Index, Numeric, String, text
from app.common.database.database import Base
from app.common.models.table_model import TableModel

from sqlalchemy.orm import relationship


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

    packaging_id = Column(
        ForeignKey("packaging.id", name="product_packaging_id_fk"),
        nullable=False,
        index=True,
    )

    packaging = relationship(
        "PackagingModel",
        primaryjoin="and_(PackagingModel.id==ProductModel.packaging_id, PackagingModel.deleted_at.is_(None))",
        lazy=True,
    )
