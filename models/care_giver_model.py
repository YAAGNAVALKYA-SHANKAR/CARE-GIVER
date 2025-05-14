from pydantic import BaseModel,Field,EmailStr
class CareGiver(BaseModel):
    """
    CareGiver model to represent a caregiver in the system.
    """
    name:str=Field(...)
    role:str=Field(...)
    email:EmailStr=Field(...)
    phone:str=Field(...,min_length=10,max_length=10)
    license_no:str=Field(...)
    assigned_facility:str=Field(...)
    permissions:str=Field(...)
    device_info:str=Field(...)