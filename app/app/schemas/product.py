from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .category import Category
from .attribute import Attribute


# Shared properties
class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    id_attribute: Optional[int]
    discount: Optional[float]
    id_category: Optional[int]
    image_thumbnail: Optional[str]
    image_url: Optional[str]
    colors_disp: Optional[str]
    size_disp: Optional[str]


# Properties to receive via API on creation
class ProductCreate(ProductBase):
    name: str
    price: float
    id_category: int
    image_url: str
    image_thumbnail: str


# Properties to receive via API on update
class ProductUpdate(ProductBase):
    pass


class ProductInDBBase(ProductBase):
    id: Optional[int]
    id_category: Optional[int]
    id_attribute: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Product(ProductInDBBase):
    category: Category
    attribute: Optional[Attribute]


# Additional properties stored in DB
class ProductInDB(ProductInDBBase):
    pass


class ResponseProduct(BaseModel):
    count: int
    data: Optional[List[Product]]
