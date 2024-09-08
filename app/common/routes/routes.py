from fastapi import APIRouter
from app.supplier.routes import supplier
from app.catalog.routes import routes as catalog
from app.stock.routes import routes as stock
from app.purchases.routes import routes as purchases
from app.receivement.routes import receivement as receivement
from app.receivement.routes import lotting as lotting

router = APIRouter()

router.include_router(router=supplier.router, prefix="/supplier", tags=["supplier"])
router.include_router(router=catalog.router, prefix="/catalog", tags=["catalog"])
router.include_router(router=stock.router, prefix="/stock", tags=["stock"])
router.include_router(router=purchases.router, prefix="/purchases", tags=["purchases"])
router.include_router(
    router=receivement.router, prefix="/receivement", tags=["receivement"]
)
router.include_router(router=lotting.router, prefix="/lotting", tags=["lotting"])
