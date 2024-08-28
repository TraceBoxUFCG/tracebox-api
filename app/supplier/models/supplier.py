from sqlalchemy import Column, ForeignKey, Index, String, text
from app.common.database.database import Base
from app.common.models.table_model import TableModel
from sqlalchemy.orm import relationship


class SupplierModel(Base, TableModel):
    __tablename__ = "supplier"
    __table_args__ = (
        Index(
            "ix_supplier_document_uniqueness",
            "document",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    document = Column(String, nullable=False)
    business_name = Column(String, nullable=False)
    address_id = Column(
        ForeignKey("address.id", name="supplier_address_id_fk"),
        nullable=False,
        index=True,
    )

    address = relationship(
        "AddressModel",
        primaryjoin="and_(AddressModel.id==SupplierModel.address_id, AddressModel.deleted_at.is_(None))",
        lazy=True,
    )
