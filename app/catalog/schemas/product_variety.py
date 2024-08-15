from pydantic import BaseModel

from app.catalog.schemas.product import Product


class ProductVarietyBase(BaseModel):
    name: str


class ProductVarietyCreate(ProductVarietyBase):
    id_product: int


class ProductVarietyUpdate(BaseModel):
    ...


class ProductVariety(ProductVarietyBase):
    id: int
    product: Product
