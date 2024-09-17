from enum import Enum
from pydantic import BaseModel
from app.catalog.schemas.packaging import Packaging
from app.catalog.schemas.product import Product
from app.receivement.schemas.asset_lot import AssetLot


class StockTransactionTypeEnum(str, Enum):
    ENTRY = "ENTRY"
    OUT = "OUT"


class StockTransactionBase(BaseModel):
    quantity: int
    product_id: int
    packaging_id: int
    type: StockTransactionTypeEnum
    meta: dict


class StockTransactionCreate(StockTransactionBase):
    @classmethod
    def from_asset_lot(cls, asset_lot: AssetLot):
        product = asset_lot.receivement_item.purchase_order_item.product_variety.product
        packaging = product.packaging

        return StockTransactionCreate(
            quantity=1 * packaging.quantity,
            product_id=product.id,
            packaging_id=packaging.id,
            type=StockTransactionTypeEnum.ENTRY,
            meta={"entry": {"from": asset_lot}},
        )


class StockTransactionUpdate(StockTransactionBase):
    ...


class StockTransaction(StockTransactionBase):
    id: int
    product: Product
    packaging: Packaging

    model_config = {"from_attributes": True}
