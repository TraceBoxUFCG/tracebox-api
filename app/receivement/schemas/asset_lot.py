from pydantic import BaseModel

from app.receivement.schemas.receivement_item import ReceivementItem
from app.stock.schemas.asset import Asset


class AssetLotBase(BaseModel):
    receivement_item_id: int
    asset_id: int


class AssetLotCreate(AssetLotBase):
    ...


class AssetLotUpdate(BaseModel):
    ...


class AssetLot(AssetLotBase):
    id: int
    receivement_item: ReceivementItem
    asset: Asset
