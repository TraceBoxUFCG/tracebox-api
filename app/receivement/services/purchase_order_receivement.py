from app.common.services.base import BaseService
from app.receivement.repositories.purchase_order_receivement import (
    PurchaseOrderReceivementRepository,
)
from app.receivement.schemas.purchase_order_receivement import (
    PurchaseOrderReceivementCreate,
    PurchaseOrderReceivementUpdate,
    PurchaseOrderReceivement,
)
from sqlalchemy.orm import Session


class PurchaseOrderReceivementService(
    BaseService[
        PurchaseOrderReceivementCreate,
        PurchaseOrderReceivementUpdate,
        PurchaseOrderReceivement,
    ]
):
    db: Session
    repository: PurchaseOrderReceivementRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=PurchaseOrderReceivementRepository)
        self.db = db
