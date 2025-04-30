from pydantic import BaseModel,Field
from datetime import time
from typing import Optional
from enum import Enum

class StatusEnum(str,Enum):
    NOT_STARTED="NOT STARTED"
    PENDING="PENDING"
    FINISHED="FINISHED"

class VisitModel(BaseModel):
    patient_id:str=Field(...)
    caregiver_id:str=Field(...)
    scheduled_time:time=Field(...)
    visit_status:StatusEnum=Field(default=StatusEnum.NOT_STARTED)
    visit_latitude:float=Field(...)
    visit_longitude:float=Field(...)
    task:list[str]=Field(...)
    remarks:str=Field(...)