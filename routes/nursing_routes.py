from fastapi import APIRouter,Depends
from services.nursing_services import NursingServices
from models.nursing_model import NursingModel
from general.security import Security
service=NursingServices()
router=APIRouter()
@router.post("/add-nursing-task")
async def add_nursing_task(nursing_data:NursingModel):
    return await service.add_nursing_task(nursing_data)
@router.get("/get-nursing-tasks")
async def get_nursing_tasks(id:str):
    return await service.get_nursing_tasks(id)