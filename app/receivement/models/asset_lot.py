from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.common.database.database import Base
from app.common.models.table_model import TableModel


class AssetLotModel(Base, TableModel):
    __tablename__ = "asset_lot"

    receivement_item_id = Column(
        Integer,
        ForeignKey(
            "receivement_item.id",
            name="asset_lot_receivement_item_id_fk",
        ),
        nullable=False,
        index=True,
    )

    receivement_item = relationship(
        "ReceivementItemModel",
        primaryjoin="and_(AssetLotModel.receivement_item_id==ReceivementItemModel.id, ReceivementItemModel.deleted_at.is_(None))",
        lazy=True,
    )

    asset_id = Column(
        Integer,
        ForeignKey(
            "asset.id",
            name="asset_lot_asset_id_fk",
        ),
        nullable=True,
        index=True,
    )

    asset = relationship(
        "AssetModel",
        primaryjoin="and_(AssetLotModel.asset_id==AssetModel.id, AssetModel.deleted_at.is_(None))",
        lazy=True,
    )
