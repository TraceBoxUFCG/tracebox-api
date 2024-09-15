from sqlalchemy import Column, ForeignKey, Index, Numeric, text
from app.common.database.database import Base
from app.common.models.table_model import TableModel
from sqlalchemy.orm import relationship


class StockModel(Base, TableModel):
    __tablename__ = "stock"

    __table_args__ = (
        Index(
            "ix_product_id_uniqueness",
            "product_id",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    quantity = Column(Numeric, nullable=False)

    product_id = Column(
        ForeignKey("product.id", name="stock_product_id_fk"),
        nullable=False,
    )

    product = relationship(
        "ProductModel",
        primaryjoin="and_(ProductModel.id==StockModel.product_id, ProductModel.deleted_at.is_(None))",
        lazy=True,
    )
