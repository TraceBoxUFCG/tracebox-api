from fastapi import Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_session
from app.supplier.services.supplier import SupplierService


def get_supplier_service(session: Session = Depends(get_session)):
    return SupplierService(db=session)
