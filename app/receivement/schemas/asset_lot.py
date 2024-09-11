from typing import Optional
from pydantic import BaseModel

from app.receivement.schemas.receivement_item import ReceivementItem
from app.stock.schemas.asset import Asset


class AssetLotBase(BaseModel):
    receivement_item_id: int
    asset_id: int


class AssetLotCreate(BaseModel):
    receivement_item_id: int


class AssetLotUpdate(BaseModel):
    asset_id: Optional[int] = None


class AssetLot(AssetLotBase):
    id: int
    receivement_item: ReceivementItem
    asset_id: Optional[int] = None
    asset: Optional[Asset] = None
