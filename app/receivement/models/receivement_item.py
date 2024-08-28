from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship

from app.common.database.database import Base
from app.common.models.table_model import TableModel


class ReceivementItemModel(Base, TableModel):
    __tablename__ = "receivement_item"

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
    )
