from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


# Shared properties
class AttributeBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


# Properties to receive via API on creation
class AttributeCreate(AttributeBase):
    name: str


# Properties to receive via API on update
class AttributeUpdate(AttributeBase):
    pass


class AttributeInDBBase(AttributeBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Attribute(AttributeInDBBase):
    pass


# Additional properties stored in DB
class AttributeInDB(AttributeInDBBase):
    pass


class ResponseAttribute(BaseModel):
    count: int
    data: Optional[List[Attribute]]
