from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .product import Product
from .user import User


# Shared properties
class ProductUserLikeBase(BaseModel):
    id_user: Optional[int]
    id_product: Optional[int]


# Properties to receive via API on creation
class ProductUserLikeCreate(ProductUserLikeBase):
    id_user: int
    id_product: int


# Properties to receive via API on update
class ProductUserLikeUpdate(ProductUserLikeBase):
    pass


class ProductUserLikeInDBBase(ProductUserLikeBase):
    id: int
    id_product: int
    id_user: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProductUserLike(ProductUserLikeInDBBase):
    product: Product
    user: User


# Additional properties stored in DB
class ProductUserLikeInDB(ProductUserLikeInDBBase):
    pass


class ResponseProductUserLike(BaseModel):
    count: int
    data: Optional[List[ProductUserLike]]
