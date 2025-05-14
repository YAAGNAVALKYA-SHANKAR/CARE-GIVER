from fastapi import FastAPI,APIRouter,UploadFile,File
from services.care_giver_services import CareGiverServices
from models.care_giver_model import CareGiver
from general.security import Security
from fastapi import Depends
service=CareGiverServices()
router=APIRouter()

"""
This module defines the routes for the CareGiver API.
It includes the following routes:
- /add-caregiver: POST route to add a new caregiver.
- /get-patient-list: GET route to get the list of patients assigned to a caregiver.
- /get-my-schedule: GET route to get the schedule of a caregiver.
""" 

@router.post("/add-caregiver")
async def add_caregiver(caregiver_data:CareGiver):return await service.add_caregiver(caregiver_data)
@router.get("/get-patient-list")
async def get_patient_list(caregiver_id:str,current_user:dict=Depends(Security.get_current_user)):return await service.patient_list(caregiver_id)
@router.get("/get-my-schedule")
async def get_my_schedule(caregiver_id:str,current_user:dict=Depends(Security.get_current_user)):return await service.my_schedule(caregiver_id)