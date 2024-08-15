from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.catalog.schemas.packaging import Packaging


class AssetStatusEnum(str, Enum):
    EMPTY = "EMPTY"
    OCCUPIED = "OCCUPIED"
    DISABLED = "DISABLED"


class AssetBase(BaseModel):
    status: AssetStatusEnum


class AssetCreate(AssetBase):
    packaging_id: Optional[int] = None


class AssetGeneratePayload(BaseModel):
    quantity: int


class AssetUpdate(BaseModel):
    status: Optional[AssetStatusEnum] = None
    packaging_id: Optional[int] = None


class Asset(AssetBase):
    id: int
    packaging: Packaging
