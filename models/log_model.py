from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional
class LogModel(BaseModel):
    patient_id:str=Field(...)
    caregiver_id:str=Field(...)
    location:list[float]=Field(...)
    vitals_id:str=Field(...)
    scheduled_visit:datetime=Field(...)
    duration:str=Field(...)
    notes:str=Field(...)