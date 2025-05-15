from pydantic import BaseModel,Field
from datetime import datetime
class VitalsModel(BaseModel):
    """
    VitalsModel to represent a patient's vitals in the system.
    """
    patient_id:str=Field(...)
    caregiver_id:str=Field(...)
    temperature:float=Field(...)
    blood_pressure:list[float]=Field(...)
    heart_rate:int=Field(...)
    respiratory_rate:int=Field(...)
    SpO2:float=Field(...)
    blood_glucose:float=Field(...)
    measured_at:datetime=Field(...)