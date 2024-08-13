from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.catalog.schemas.product import Product, ProductCreate, ProductListParams
from app.catalog.services.product import ProductService

from fastapi_pagination.ext.sqlalchemy import paginate

from app.supplier.deps import get_product_service


router = APIRouter()


@router.post("/", response_model=Product)
def create_product(
    payload: ProductCreate, service: ProductService = Depends(get_product_service)
):
    return service.create(create=payload)


@router.get("/", response_model=Page[Product])
def get_all_products(
    params: ProductListParams = Depends(),
    service: ProductService = Depends(get_product_service),
):
    return paginate(service.get_all_for_pagination(params=params))


@router.get("/{id}", response_model=Product)
def get_product_by_id(id: int, service: ProductService = Depends(get_product_service)):
    return service.get_by_id(id=id)


@router.delete("/{id}")
def delete_product(id: int, service: ProductService = Depends(get_product_service)):
    return service.delete(id=id)
