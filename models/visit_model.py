from pydantic import BaseModel,Field
from datetime import time
from typing import Optional
from enum import Enum
class StatusEnum(str,Enum):
    ACTIVE="DONE"
    INACTIVE="PENDING"
class VisitModel(BaseModel):
    patient_id:str=Field(...)
    caregiver_id:str=Field(...)
    scheduled_time:time=Field(...)
    visit_status:StatusEnum.INACTIVE
    location:list[str]=Field(...)
    start_time:Optional[time]=Field(...)
    end_time:Optional[time]=Field(...)
    remarks:str=Field(...)