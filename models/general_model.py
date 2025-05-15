from pydantic import BaseModel,Field
class Documentation(BaseModel):
    visit_id:str=Field(...)
    documentation_type:str=Field(...)
    description:str=Field(...)
    
