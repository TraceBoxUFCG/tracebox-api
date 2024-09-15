from fastapi import APIRouter
from app.stock.routes import asset, stock

router = APIRouter()

router.include_router(router=stock.router, tags=["stock"])
router.include_router(router=asset.router, prefix="/asset", tags=["asset"])
