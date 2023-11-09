from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


# Shared properties
class CategoryBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


# Properties to receive via API on creation
class CategoryCreate(CategoryBase):
    name: str


# Properties to receive via API on update
class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Category(CategoryInDBBase):
    pass


# Additional properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass


class ResponseCategory(BaseModel):
    count: int
    data: Optional[List[Category]]
