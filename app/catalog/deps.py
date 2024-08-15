from fastapi import Depends
from app.catalog.services.product import ProductService
from app.catalog.services.product_variety import ProductVarietyService
from app.common.dependencies import get_session
from sqlalchemy.orm import Session


def get_product_service(session: Session = Depends(get_session)):
    return ProductService(db=session)


def get_product_variety_service(session: Session = Depends(get_session)):
    return ProductVarietyService(db=session)
