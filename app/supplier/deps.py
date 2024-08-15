from fastapi import Depends
from sqlalchemy.orm import Session

from app.catalog.services.product import ProductService
from app.common.dependencies import get_session
from app.stock.services.asset import AssetService
from app.supplier.services.supplier import SupplierService


def get_supplier_service(session: Session = Depends(get_session)):
    return SupplierService(db=session)


def get_product_service(session: Session = Depends(get_session)):
    return ProductService(db=session)


def get_asset_service(session: Session = Depends(get_session)):
    return AssetService(db=session)
