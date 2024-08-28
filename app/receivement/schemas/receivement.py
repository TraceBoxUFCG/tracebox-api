from pydantic import BaseModel


class ReceiveItemPayload(BaseModel):
    received_quantity: int
    rejected_quantity: int
