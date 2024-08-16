from datetime import date
from typing import Optional
from sqlalchemy.orm import Session

from app.common.repositories.base import BaseFinder, BaseRepository
from app.purchases.models.purchase_order import PurchaseOrderModel
from app.purchases.schemas.purchase_order import PurchaseOrderStatusEnum
from app.supplier.models.supplier import SupplierModel


class PurchaseOrderFinder(BaseFinder[PurchaseOrderModel]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls(
            db.query(PurchaseOrderModel).filter(PurchaseOrderModel.deleted_at.is_(None))
        )

    def filter_by_status(self, status: Optional[PurchaseOrderStatusEnum] = None):
        if status:
            return PurchaseOrderFinder(
                (self.base_query.filter(PurchaseOrderModel.status == status))
            )
        return self

    def filter_by_expected_arrival_date(
        self, expected_arrival_date: Optional[date] = None
    ):
        if expected_arrival_date:
            return PurchaseOrderFinder(
                (
                    self.base_query.filter(
                        PurchaseOrderModel.expected_arrival_date
                        == expected_arrival_date
                    )
                )
            )

        return self

    def filtered_by_supplier_business_name_ilike(self, target: Optional[str] = None):
        if target:
            return PurchaseOrderFinder(
                (
                    self.base_query.filter(
                        SupplierModel.business_name.ilike(f"%{target.strip()}%")
                    )
                )
            )
        return self

    def search_by_query_criterias(self, target: str):
        self.base_query = self.base_query.join(
            SupplierModel, SupplierModel.id == PurchaseOrderModel.supplier_id
        ).filter(SupplierModel.deleted_at.is_(None))
        business_name_query = self.filtered_by_supplier_business_name_ilike(
            target=target
        ).base_query

        return PurchaseOrderFinder(business_name_query)


class PurchaseOrderRepository(
    BaseRepository[PurchaseOrderModel, int],
):
    finder: PurchaseOrderFinder

    def __init__(self, db: Session):
        super().__init__(
            PurchaseOrderModel.id,
            model_class=PurchaseOrderModel,
            finder=PurchaseOrderFinder,
            db=db,
        )
