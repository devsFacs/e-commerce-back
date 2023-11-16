from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .user import User
from .product import Product


# Shared properties
class UserProductBase(BaseModel):
    id_user: Optional[int]
    id_product: Optional[int]
    quantity: Optional[int]


# Properties to receive via API on creation
class UserProductCreate(UserProductBase):
    id_user: int
    id_product: int
    quantity: int


# Properties to receive via API on update
class UserProductUpdate(UserProductBase):
    pass


class UserProductInDBBase(UserProductBase):
    id: int
    id_user: int
    id_product: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserProduct(UserProductInDBBase):
    user: User
    product: Product


# Additional properties stored in DB
class UserProductInDB(UserProductInDBBase):
    pass


class ResponseUserProduct(BaseModel):
    count: int
    data: Optional[List[UserProduct]]
