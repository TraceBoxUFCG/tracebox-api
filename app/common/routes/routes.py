from fastapi import APIRouter
from app.supplier.routes import supplier
from app.catalog.routes import routes as catalog

router = APIRouter()

router.include_router(router=supplier.router, prefix="/supplier", tags=["supplier"])
router.include_router(router=catalog.router, prefix="/catalog", tags=["catalog"])
