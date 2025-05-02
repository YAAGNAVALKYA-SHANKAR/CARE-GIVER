from pydantic import BaseModel,Field,EmailStr
class CareGiver(BaseModel):
    name:str=Field(...)
    role:str=Field(...)
    email:EmailStr=Field(...)
    phone:int=Field(...,min_length=10,max_length=10)
    license_no:str=Field(...)
    assigned_facility:str=Field(...)
    permissions:str=Field(...)
    device_info:str=Field(...)