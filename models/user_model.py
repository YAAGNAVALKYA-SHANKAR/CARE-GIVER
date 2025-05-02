from typing import Optional
from pydantic import BaseModel,EmailStr,Field

class UserModel(BaseModel):
    username:str=Field(...)
    email:EmailStr=Field(...)
    phone:str=Field(...,min_length=10,max_length=10)
    is_active:bool=True
    password:str=Field(...,min_length=8)
    role:Optional[str]="user"
    class Config:
        orm_mode = True