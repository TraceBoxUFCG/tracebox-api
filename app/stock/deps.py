from fastapi import Depends
from app.common.dependencies import get_session
from app.stock.services.asset import AssetService
from sqlalchemy.orm import Session

from app.stock.services.stock import StockService


def get_asset_service(session: Session = Depends(get_session)):
    return AssetService(db=session)


def get_stock_service(session: Session = Depends(get_session)):
    return StockService(db=session)
