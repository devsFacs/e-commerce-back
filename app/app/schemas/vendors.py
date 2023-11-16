from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .user import User


# Shared properties
class VendorsBase(BaseModel):
    name: Optional[str]
    address: Optional[str]
    logo_url: Optional[str]
    logo_thumbnail: Optional[str]
    id_user: Optional[int]
    code_promo: Optional[str]
    date_validation: Optional[date]
    latitude: Optional[str]
    longitude: Optional[str]


# Properties to receive via API on creation
class VendorsCreate(VendorsBase):
    name: str
    address: str
    id_user: int


# Properties to receive via API on update
class VendorsUpdate(VendorsBase):
    pass


class VendorsInDBBase(VendorsBase):
    id: int
    id_user: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Vendors(VendorsInDBBase):
    user: User


# Additional properties stored in DB
class VendorsInDB(VendorsInDBBase):
    pass


class ResponseVendors(BaseModel):
    count: int
    data: Optional[List[Vendors]]
