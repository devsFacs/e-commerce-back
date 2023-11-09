from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .product import Product
from .user import User


# Shared properties
class ProductUserViewBase(BaseModel):
    id_user: Optional[int]
    id_product: Optional[int]


# Properties to receive via API on creation
class ProductUserViewCreate(ProductUserViewBase):
    id_user: int
    id_product: int


# Properties to receive via API on update
class ProductUserViewUpdate(ProductUserViewBase):
    pass


class ProductUserViewInDBBase(ProductUserViewBase):
    id: int
    id_product: int
    id_user: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProductUserView(ProductUserViewInDBBase):
    product: Product
    user: User


# Additional properties stored in DB
class ProductUserViewInDB(ProductUserViewInDBBase):
    pass


class ResponseProductUserView(BaseModel):
    count: int
    data: Optional[List[ProductUserView]]
