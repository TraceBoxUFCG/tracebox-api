from enum import Enum


class AssetStatusEnum(str, Enum):
    EMPTY = "EMPTY"
    OCCUPIED = "OCCUPIED"
    DISABLED = "DISABLED"
