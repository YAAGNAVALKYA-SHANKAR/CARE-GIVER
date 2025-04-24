from fastapi import APIRouter
from services.patient_service import PatientServices
from models.patient_model import PatientModel

service=PatientServices()
router=APIRouter()

@router.post("/add-patient")
async def add_patient(patient_data:PatientModel):
    return await service.add_patient(patient_data)

@router.get("search-patient/{patient_id}")
async def search_patient(patient_id:str):
    return await service.find_patient(patient_id)