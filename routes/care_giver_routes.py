from fastapi import FastAPI,APIRouter, UploadFile, File
from services.care_giver_services import CareGiverServices
from models.care_giver_model import CareGiver
service=CareGiverServices()
router=APIRouter()
@router.post("/add-caregiver")
async def add_caregiver(caregiver_data:CareGiver):
    return await service.add_caregiver(caregiver_data)

@router.get("/get-patient-list")
async def get_patient_list(caregiver_id:str):
    return await service.patient_list(caregiver_id)

@router.get("/get-my-schedule")
async def get_my_schedule(caregiver_id:str):
    return await service.my_schedule(caregiver_id)