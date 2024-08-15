from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_pagination import Page

from fastapi_pagination.ext.sqlalchemy import paginate

from app.catalog.deps import get_product_variety_service
from app.catalog.schemas.product_variety import ProductVariety, ProductVarietyListParams
from app.catalog.services.product_variety import ProductVarietyService


router = APIRouter()


@router.post("/import", response_model=List[ProductVariety])
async def import_product_variety(
    file: UploadFile = File(),
    service: ProductVarietyService = Depends(get_product_variety_service),
):
    return await service.import_from_csv(file=file)


@router.get("/", response_model=Page[ProductVariety])
def get_all_product_variety(
    params: ProductVarietyListParams = Depends(),
    service: ProductVarietyService = Depends(get_product_variety_service),
):
    return paginate(service.get_all_for_pagination(params=params))


@router.delete("/{id}")
def delete_product_variety(
    id: int,
    service: ProductVarietyService = Depends(get_product_variety_service),
):
    service.delete(id=id)
