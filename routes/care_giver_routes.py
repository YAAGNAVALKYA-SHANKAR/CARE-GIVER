from fastapi import FastAPI,APIRouter, UploadFile, File
from services.care_giver_services import CareGiverServices
from models.care_giver_model import CareGiver
service=CareGiverServices()
router=APIRouter()
@router.post("/add-caregiver")
async def add_caregiver(caregiver_data:CareGiver):
    return await service.add_caregiver(caregiver_data)