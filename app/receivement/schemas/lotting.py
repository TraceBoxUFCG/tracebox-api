from pydantic import BaseModel


class LotReceivementItemPayload(BaseModel):
    receivement_item_id: int
    asset_id: int
