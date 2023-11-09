from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .category import Category


# Shared properties
class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    attribute: Optional[str]
    discount: Optional[float]
    code_promo: Optional[str]
    id_category: Optional[int]
    valid_code_start: Optional[datetime]
    valid_code_end: Optional[datetime]
    image_thumbnail: Optional[str]
    image_url: Optional[str]


# Properties to receive via API on creation
class ProductCreate(ProductBase):
    name: str
    description: Optional[str]
    price: float
    image_url: str
    image_thumbnail: str


# Properties to receive via API on update
class ProductUpdate(ProductBase):
    pass


class ProductInDBBase(ProductBase):
    id: Optional[int]
    id_category: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Product(ProductInDBBase):
    category: Category


# Additional properties stored in DB
class ProductInDB(ProductInDBBase):
    pass


class ResponseProduct(BaseModel):
    count: int
    data: Optional[List[Product]]
