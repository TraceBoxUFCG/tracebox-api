from sqlalchemy import (
    Column,
    Enum,
    Index,
    Integer,
    ForeignKey,
    Numeric,
    text,
)
from sqlalchemy.orm import relationship

from app.common.database.database import Base
from app.common.models.table_model import TableModel
from app.receivement.schemas.receivement_item import ReceivementItemStatusEnum


class ReceivementItemModel(Base, TableModel):
    __tablename__ = "receivement_item"

    __table_args__ = (
        Index(
            "ix_purchase_order_item_id_uniqueness",
            "purchase_order_item_id",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    purchase_order_item_id = Column(
        Integer,
        ForeignKey(
            "purchase_order_item.id",
            name="receivement_item_purchase_order_item_id_fk",
        ),
        nullable=False,
        index=True,
    )

    received_quantity = Column(Numeric, nullable=False)

    rejected_quantity = Column(Numeric, nullable=False)

    purchase_order_item = relationship(
        "PurchaseOrderItemModel",
        primaryjoin="and_(ReceivementItemModel.purchase_order_item_id==PurchaseOrderItemModel.id, PurchaseOrderItemModel.deleted_at.is_(None))",
        lazy=True,
    )

    status = Column(
        Enum(ReceivementItemStatusEnum),
        nullable=False,
        server_default=ReceivementItemStatusEnum.PENDING,
    )
