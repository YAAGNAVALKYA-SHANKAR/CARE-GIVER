from pydantic import BaseModel, Field
from typing import Optional

class NursingModel(BaseModel):
    id:str=Field(..., title="ID", description="Unique identifier for the nursing task")
    description: str = Field(..., title="Description", description="Description of the nursing task")