from pydantic import BaseModel,Field
from datetime import datetime
class LogModel(BaseModel):
    """
    LogModel to represent a log entry in the system.
    """
    patient_id:str=Field(...)
    caregiver_id:str=Field(...)
    visit_id:str=Field(...)
    location:list[float]=Field(...)
    vitals_id:str=Field(...)
    scheduled_visit:datetime=Field(...)
    duration:str=Field(...)
    clinical_notes:str=Field(...)
    acknowledgement:list[bool]