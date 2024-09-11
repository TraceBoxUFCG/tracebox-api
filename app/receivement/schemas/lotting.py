from pydantic import BaseModel


class LotReceivementItemPayload(BaseModel):
    asset_id: int
