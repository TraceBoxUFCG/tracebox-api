from fastapi import Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_session
from app.purchases.services.purchase_order import PurchaseOrderService


def get_purchase_order_service(session: Session = Depends(get_session)):
    return PurchaseOrderService(db=session)
