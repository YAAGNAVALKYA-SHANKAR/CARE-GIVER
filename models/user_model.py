from typing import Optional
from pydantic import BaseModel,EmailStr,Field
class UserModel(BaseModel):
    """
    User model to represent a user in the system.
    """
    username:str=Field(...)
    email:EmailStr=Field(...)
    phone:str=Field(...,min_length=10,max_length=10)
    is_active:bool=True
    password:str=Field(...,min_length=8)
    role:Optional[str]="user"
    class Config:
        orm_mode = True
class SignupModel(BaseModel):
    email:EmailStr=Field(...)
    password:str=Field(...,min_length=8)
    confirm_password:str=Field(...,min_length=8)
    class Config:
        orm_mode = True