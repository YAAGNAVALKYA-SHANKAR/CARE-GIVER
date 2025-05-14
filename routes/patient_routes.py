from fastapi import APIRouter
from fastapi import Depends
from general.security import Security
from services.patient_service import PatientServices
from models.patient_model import PatientModel
service=PatientServices()
router=APIRouter()

"""
This module defines the routes for the Patient API.
It includes the following routes:
- /add-patient: POST route to add a new patient.
- /search-patient: GET route to search for a patient by ID.
"""

@router.post("/add-patient")
async def add_patient(patient_data:PatientModel):return await service.add_patient(patient_data)
@router.get("/search-patient/{patient_id}")
async def get_patient(patient_id:str,current_user:dict=Depends(Security.get_current_user)):return await service.find_patient(patient_id)