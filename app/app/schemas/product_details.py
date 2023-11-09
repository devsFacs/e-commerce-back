from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .product import Product


# Shared properties
class ProductDetailsBase(BaseModel):
    color: Optional[str]
    id_product: Optional[str]
    size: Optional[str]
    status_stock: Optional[int]


# Properties to receive via API on creation
class ProductDetailsCreate(ProductDetailsBase):
    color: str
    id_product: int
    size: str
    status_stock: int


# Properties to receive via API on update
class ProductDetailsUpdate(ProductDetailsBase):
    pass


class ProductDetailsInDBBase(ProductDetailsBase):
    id: int
    id_product: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProductDetails(ProductDetailsInDBBase):
    product: Product


# Additional properties stored in DB
class ProductDetailsInDB(ProductDetailsInDBBase):
    pass


class ResponseProductDetails(BaseModel):
    count: int
    data: Optional[List[ProductDetails]]
