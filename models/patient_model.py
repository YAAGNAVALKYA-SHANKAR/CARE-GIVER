from pydantic import BaseModel,Field
from typing import Optional
class PatientModel(BaseModel):
    """
    PatientModel to represent a patient in the system.
    """
    cpr_id:str=Field(...)
    name:str=Field(...)
    age:str=Field(...)
    gender:str=Field(...)
    address:str=Field(...)
    allergies:Optional[list[str]]=Field(...)
    chronic_conditions:Optional[list[str]]=Field(...)
    current_medications:Optional[list[str]]=Field(...)
    assigned_caregivers:Optional[list[str]]=Field(...)