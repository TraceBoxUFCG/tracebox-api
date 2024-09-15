from app.receivement.schemas.asset_lot import AssetLot
from app.stock.schemas.stock import Stock, StockCreate, StockUpdate
from app.stock.schemas.stock_transaction import StockTransactionCreate
from app.stock.services.stock import StockService
from app.stock.services.stock_transaction import StockTransactionService
from sqlalchemy.orm import Session


class StockManagementService:
    stock_transaction_service: StockTransactionService
    stock_service: StockService

    def __init__(self, db: Session) -> None:
        self.stock_transaction_service = StockTransactionService(db=db)
        self.stock_service = StockService(db=db)

    def add_from_lotting(self, asset_lot: AssetLot) -> Stock:
        product_id = (
            asset_lot.receivement_item.purchase_order_item.product_variety.product.id
        )
        transaction_create = StockTransactionCreate.from_asset_lot(asset_lot=asset_lot)
        stock_transaction = self.stock_transaction_service.create(
            create=transaction_create
        )
        stock = self.stock_service.get_by_product_id(product_id=product_id)

        if stock:
            stock_update = StockUpdate(
                quantity=stock.quantity + stock_transaction.quantity
            )
            return self.stock_service.update(update=stock_update, id=stock.id)
        else:
            stock_create = StockCreate(
                product_id=product_id, quantity=stock_transaction.quantity
            )
            return stock_create
