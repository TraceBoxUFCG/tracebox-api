from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship

from app.common.database.database import Base
from app.common.models.table_model import TableModel


class PurchaseOrderItemModel(Base, TableModel):
    __tablename__ = "purchase_order_item"

    purchase_order_id = Column(
        Integer,
        ForeignKey(
            "purchase_order.id", name="purchase_order_item_purchase_order_id_fk"
        ),
        nullable=False,
        index=True,
    )
    product_variety_id = Column(
        Integer,
        ForeignKey(
            "product_variety.id", name="purchase_order_item_product_variety_id_fk"
        ),
        nullable=False,
        index=True,
    )

    boxes_quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric, nullable=False)

    purchase_order = relationship(
        "PurchaseOrderModel",
        primaryjoin="and_(PurchaseOrderItemModel.purchase_order_id==PurchaseOrderModel.id, PurchaseOrderModel.deleted_at.is_(None))",
        back_populates="items",
        lazy=True,
    )

    product_variety = relationship(
        "ProductVarietyModel",
        primaryjoin="and_(ProductVarietyModel.id==PurchaseOrderItemModel.product_variety_id, ProductVarietyModel.deleted_at.is_(None))",
        lazy=True,
    )

    receivement = relationship(
        "ReceivementItem",
        primaryjoin="and_(ReceivementItem.purchase_order_item_id==PurchaseOrderItemModel.id, ReceivementItem.deleted_at.is_(None))",
        viewonly=True,
        lazy=True,
    )
