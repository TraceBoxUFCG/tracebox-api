from sqlalchemy import Column, ForeignKey, Index, String, text
from app.common.database.database import Base
from app.common.models.table_model import TableModel

from sqlalchemy.orm import relationship


class ProductVarietyModel(Base, TableModel):
    __tablename__ = "product_variety"
    __table_args__ = (
        Index(
            "ix_product_variety_name_uniqueness",
            "name",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    name = Column(String, nullable=False)

    product_id = Column(
        ForeignKey("product.id", name="product_variety_product_id_fk"),
        nullable=False,
        index=True,
    )

    product = relationship(
        "ProductModel",
        primaryjoin="and_(ProductModel.id==ProductVarietyModel.product_id, ProductModel.deleted_at.is_(None))",
        lazy=True,
    )
