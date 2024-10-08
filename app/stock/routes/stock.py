from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.stock.deps import get_stock_service
from app.stock.schemas.stock import Stock, StockDetail, StockListParams
from app.stock.services.stock import StockService
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter()


@router.get("/", response_model=Page[Stock])
def get_stock(
    params: StockListParams = Depends(),
    service: StockService = Depends(get_stock_service),
):
    return paginate(service.get_all_for_pagination(params=params))


@router.get("/{product_id}/details", response_model=StockDetail)
def get_stock_details(
    product_id: int,
    service: StockService = Depends(get_stock_service),
):
    return service.get_stock_details(product_id=product_id)
