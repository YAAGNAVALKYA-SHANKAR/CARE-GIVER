from pydantic import BaseModel,Field
from datetime import time
from typing import Optional
class VisitModel(BaseModel):
    patient_id:str=Field(...)
    caregiver_id:str=Field(...)
    scheduled_time:time=Field(...)
    visit_status:str=Field(...)
    location:list[str]=Field(...)
    start_time:Optional[time]=Field(...)
    end_time:Optional[time]=Field(...)
    remarks:str=Field(...)



#visit_id, patient_id, caregiver_id, scheduled_time, status (pending/in-progress/completed), location, start_time, end_time, remarks 