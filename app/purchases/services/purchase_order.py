from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.common.services.base import BaseService
from app.purchases.repositories.purchase_order import PurchaseOrderRepository
from app.purchases.schemas.purchase_order import (
    PurchaseOrder,
    PurchaseOrderCreate,
    PurchaseOrderCreateOrUpdate,
    PurchaseOrderListParams,
    PurchaseOrderStatusEnum,
    PurchaseOrderUpdate,
)
from app.purchases.schemas.purchase_order_item import PurchaseOrderItemCreate
from app.purchases.services.purchase_order_item import PurchaseOrderItemService


class PurchaseOrderService(
    BaseService[PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrder]
):
    db: Session
    repository: PurchaseOrderRepository
    purchase_order_item_service: PurchaseOrderItemService

    def __init__(self, db: Session):
        super().__init__(
            db=db, repository=PurchaseOrderRepository, return_model=PurchaseOrder
        )
        self.db = db
        self.purchase_order_item_service = PurchaseOrderItemService(db=db)

    def place(self, create_or_update: PurchaseOrderCreateOrUpdate) -> PurchaseOrder:
        existing_order = (
            self.get_by_id(id=create_or_update.id) if create_or_update.id else None
        )

        if existing_order:
            if existing_order.status != PurchaseOrderStatusEnum.DRAFT:
                raise HTTPException(
                    status_code=409, detail="Cant update order that is not in draft"
                )

            update_data = PurchaseOrderUpdate(
                expected_arrival_date=create_or_update.expected_arrival_date,
            )

            self.purchase_order_item_service.place(
                purchase_order_id=existing_order.id, items=create_or_update.items
            )

            return self.update(id=create_or_update.id, update=update_data)

        else:
            create = PurchaseOrderCreate(
                supplier_id=create_or_update.supplier_id,
                expected_arrival_date=create_or_update.expected_arrival_date,
            )
            created_purchase_order = self.create(create=create)
            [
                self.purchase_order_item_service.create(
                    PurchaseOrderItemCreate(
                        boxes_quantity=item.boxes_quantity,
                        unit_price=item.boxes_quantity,
                        product_variety_id=item.product_variety_id,
                        purchase_order_id=created_purchase_order.id,
                    )
                )
                for item in create_or_update.items
            ]

            return created_purchase_order

    def _get_all_query(
        self, params: PurchaseOrderListParams
    ) -> PurchaseOrderListParams:
        filtered = self.repository.finder

        if params.q:
            filtered = filtered.search_by_query_criterias(target=params.q)

        if params.status:
            filtered = filtered.filter_by_status(status=params.status)

        if params.expected_arrival_date:
            filtered = filtered.filter_by_expected_arrival_date(
                expected_arrival_date=params.expected_arrival_date
            )

        return filtered

    def get_all_for_pagination(self, params: PurchaseOrderListParams):
        return self._get_all_query(params=params).query

    def confirm(self, id: int):
        purchase_order = self.get_by_id(id=id)
        if purchase_order.status != PurchaseOrderStatusEnum.DRAFT:
            raise HTTPException(
                status_code=409,
                detail="Cant confirm purchase order that is not in draft",
            )

        update_payload = PurchaseOrderUpdate(status=PurchaseOrderStatusEnum.CONFIRMED)
        return self.update(id=id, update=update_payload)

    def start_receivement(self, id: int):
        purchase_order = self.get_by_id(id=id)
        if purchase_order.status != PurchaseOrderStatusEnum.CONFIRMED:
            raise HTTPException(
                status_code=409,
                detail="Cant start receivement for a purchase order that is not confirmed",
            )

        update_payload = PurchaseOrderUpdate(
            status=PurchaseOrderStatusEnum.RECEIVEMENT_STARTED
        )
        return self.update(id=id, update=update_payload)

    def finish_receivement(self, id: int):
        purchase_order = self.get_by_id(id=id)
        if purchase_order.status != PurchaseOrderStatusEnum.RECEIVEMENT_STARTED:
            raise HTTPException(
                status_code=409,
                detail="Cant finish receivement for a purchase order that did not started receivement process",
            )

        update_payload = PurchaseOrderUpdate(status=PurchaseOrderStatusEnum.RECEIVED)
        return self.update(id=id, update=update_payload)

    def start_lotting(self, id: int):
        purchase_order = self.get_by_id(id=id)
        if purchase_order.status != PurchaseOrderStatusEnum.RECEIVED:
            raise HTTPException(
                status_code=409,
                detail="Cant start lotting for a purchase order that is not received",
            )

        update_payload = PurchaseOrderUpdate(
            status=PurchaseOrderStatusEnum.LOTTING_STARTED
        )
        return self.update(id=id, update=update_payload)

    def finish_lotting(self, id: int):
        purchase_order = self.get_by_id(id=id)
        if purchase_order.status != PurchaseOrderStatusEnum.LOTTING_STARTED:
            raise HTTPException(
                status_code=409,
                detail="Cant finish lotting for a purchase order that did not started lotting process",
            )

        update_payload = PurchaseOrderUpdate(status=PurchaseOrderStatusEnum.LOTTED)
        return self.update(id=id, update=update_payload)
