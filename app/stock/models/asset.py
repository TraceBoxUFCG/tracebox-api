from sqlalchemy import Column, Enum, ForeignKey
from app.common.database.database import Base
from app.common.models.table_model import TableModel
from sqlalchemy.orm import relationship

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

    packaging = relationship(
        "PackagingModel",
        primaryjoin="and_(PackagingModel.id==AssetModel.packaging_id, PackagingModel.deleted_at.is_(None))",
        backref="asset",
    )
