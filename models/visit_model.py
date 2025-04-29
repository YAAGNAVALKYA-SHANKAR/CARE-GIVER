from pydantic import BaseModel,Field
from datetime import time
from typing import Optional
from enum import Enum

class StatusEnum(str,Enum):
    PENDING="PENDING"
    IN_PROGRESS="IN PROGRESS"
    FINISHED="FINISHED"

class VisitModel(BaseModel):
    patient_id:str=Field(...)
    caregiver_id:str=Field(...)
    scheduled_time:time=Field(...)
    visit_status:StatusEnum=Field(default=StatusEnum.PENDING)
    visit_latitude:float
    visit_longitude:float
    start_time:Optional[time]=Field(...)
    end_time:Optional[time]=Field(...)
    remarks:str=Field(...)
