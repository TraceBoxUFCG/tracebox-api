from sqlalchemy import (
    Column,
    Enum,
    Integer,
    ForeignKey,
    Date,
)
from sqlalchemy.orm import relationship

from app.common.database.database import Base
from app.common.models.table_model import TableModel
from app.purchases.schemas.purchase_order import PurchaseOrderStatusEnum


class PurchaseOrderModel(Base, TableModel):
    __tablename__ = "purchase_order"

    supplier_id = Column(
        Integer,
        ForeignKey("supplier.id", name="purchase_order_supplier_id_fk"),
        nullable=False,
        index=True,
    )
    expected_arrival_date = Column(Date, nullable=False)

    status = Column(
        Enum(PurchaseOrderStatusEnum),
        nullable=False,
        server_default=PurchaseOrderStatusEnum.DRAFT,
    )
    supplier = relationship(
        "SupplierModel",
        primaryjoin="and_(SupplierModel.id==PurchaseOrderModel.supplier_id, SupplierModel.deleted_at.is_(None))",
        backref="purchase_orders",
    )

    items = relationship(
        "PurchaseOrderItemModel",
        primaryjoin="and_(PurchaseOrderItemModel.purchase_order_id==PurchaseOrderModel.id, PurchaseOrderItemModel.deleted_at.is_(None))",
        back_populates="purchase_order",
    )
