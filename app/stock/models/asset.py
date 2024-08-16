from sqlalchemy import Column, Enum, ForeignKey
from app.catalog.models.product import ProductModel
from app.common.database.database import Base
from app.common.models.table_model import TableModel
from sqlalchemy.orm import relationship, foreign

from app.stock.schemas.asset import AssetStatusEnum


class AssetModel(Base, TableModel):
    __tablename__ = "asset"

    status = Column(
        Enum(AssetStatusEnum), nullable=False, server_default=AssetStatusEnum.EMPTY
    )

    packaging_id = Column(
        ForeignKey("packaging.id", name="asset_packaging_id_fk"),
        nullable=True,
    )

    product = relationship(
        "ProductModel",
        primaryjoin=packaging_id == foreign(ProductModel.packaging_id),
        viewonly=True,
        uselist=False,
    )
