from pydantic import BaseModel,Field
from datetime import time
from enum import Enum
class StatusEnum(str,Enum):
    """
    Enum for visit status.
    """
    NOT_STARTED="NOT STARTED"
    PENDING="PENDING"
    FINISHED="FINISHED"
class VisitModel(BaseModel):
    """
    VisitModel to represent a visit in the system.
    """
    patient_id:str=Field(...)
    caregiver_id:str=Field(...)
    scheduled_time:time=Field(...)
    visit_status:StatusEnum=Field(default=StatusEnum.NOT_STARTED)
    visit_latitude:float=Field(...)
    visit_longitude:float=Field(...)
    task:list[str]=Field(...)
    remarks:str=Field(...)

class SummaryModel(BaseModel):
    """
    SummaryModel to represent the summary of a visit in the system
    """
    patient_id:str=Field(...)
    visit_id:str=Field(...)
    vitals_id:str=Field(...)
    doc_id:str=Field(...)