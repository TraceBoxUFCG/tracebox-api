from sqlalchemy import JSON, Column, Enum, ForeignKey, Numeric, text
from app.common.database.database import Base
from app.common.models.table_model import TableModel
from sqlalchemy.orm import relationship

from app.stock.schemas.stock_transaction import StockTransactionTypeEnum


class StockTransactionModel(Base, TableModel):
    __tablename__ = "stock_transaction"

    quantity = Column(Numeric, nullable=False)

    product_id = Column(
        ForeignKey("product.id", name="stock_transaction_product_id_fk"),
        nullable=False,
    )

    product = relationship(
        "ProductModel",
        primaryjoin="and_(ProductModel.id==StockTransactionModel.product_id, ProductModel.deleted_at.is_(None))",
        lazy=True,
    )

    packaging_id = Column(
        ForeignKey("product.id", name="stock_transaction_packaging_id_fk"),
        nullable=False,
    )

    packaging = relationship(
        "PackagingModel",
        primaryjoin="and_(PackagingModel.id==StockTransactionModel.product_id, PackagingModel.deleted_at.is_(None))",
        lazy=True,
    )

    type = Column(
        Enum(StockTransactionTypeEnum),
        nullable=False,
    )

    meta = Column(JSON, nullable=False, server_default=text("'{}'"))
