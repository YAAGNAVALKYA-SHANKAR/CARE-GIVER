from pydantic import BaseModel,Field

class CareGiver(BaseModel):
    name:str=Field(...)
    role:str=Field(...)
    license_no:str=Field(...)
    assigned_facility:str=Field(...)
    permissions:str=Field(...)
    device_info:str=Field(...)