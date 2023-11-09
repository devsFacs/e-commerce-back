from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .vendors import Vendors
from .product import Product


# Shared properties
class VendorsProductBase(BaseModel):
    id_vendor: Optional[int]
    id_product: Optional[int]


# Properties to receive via API on creation
class VendorsProductCreate(VendorsProductBase):
    id_vendor: int
    id_product: int


# Properties to receive via API on update
class VendorsProductUpdate(VendorsProductBase):
    pass


class VendorsProductInDBBase(VendorsProductBase):
    id: int
    id_vendor: int
    id_product: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class VendorsProduct(VendorsProductInDBBase):
    vendor: Vendors
    product: Product


# Additional properties stored in DB
class VendorsProductInDB(VendorsProductInDBBase):
    pass


class ResponseVendorsProduct(BaseModel):
    count: int
    data: Optional[List[VendorsProduct]]
