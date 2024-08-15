from fastapi import Depends
from app.common.dependencies import get_session
from app.stock.services.asset import AssetService
from sqlalchemy.orm import Session


def get_asset_service(session: Session = Depends(get_session)):
    return AssetService(db=session)
