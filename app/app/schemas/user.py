from typing import List, Optional
from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_vendors: Optional[bool]
    is_superuser: bool = False
    first_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]
    type_auth: Optional[str]
    mobile: Optional[str]
    sex: Optional[str]
    id_google: Optional[str]
    id_facebook: Optional[str]
    last_name: Optional[str]


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    first_name: str
    last_name: Optional[str]
    address: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UserLogin(BaseModel):
    email: Optional[EmailStr]
    type_auth: Optional[str] = "google"
    id_google: Optional[str]
    id_facebook: Optional[str]


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class ResponseUser(BaseModel):
    count: int
    data: Optional[List[User]]
