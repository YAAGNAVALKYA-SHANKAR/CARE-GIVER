from fastapi import APIRouter,Depends, UploadFile, File
from services.visit_services import VisitServices
from models.log_model import LogModel
from models.visit_model import VisitModel
from models.vitals_model import VitalsModel
from general.security import Security
router=APIRouter()
service=VisitServices()

@router.post("/add-visit")
async def add_visit(visit_data:VisitModel):return await service.add_visit(visit_data)

@router.post("/add-visit-details.{caregiver_id}")
async def add_visit_details(visit_data:VisitModel,current_user:dict=Depends(Security.get_current_user)):return await service.add_visit_details(visit_data)

@router.post("/add-vitals/{patient_id}")
async def add_vitals(vitals_data:VitalsModel,current_user:dict=Depends(Security.get_current_user)):return await service.add_vitals(vitals_data)

@router.get("/mark-arrival/{visit_id}")
async def mark_arrival(visit_id:str,current_lat:float,current_long:float,selfie:UploadFile=File(...),current_user:dict=Depends(Security.get_current_user)):return await service.mark_arrival(visit_id,current_lat,current_long,selfie)

@router.get("/start-visit/{visit_id}")
async def start_visit(visit_id:str,current_user:dict=Depends(Security.get_current_user)):return await service.start_visit(visit_id)

@router.post("/finish-visit/{visit_id}")
async def finish_visit(log_data:LogModel,current_user:dict=Depends(Security.get_current_user)):return await service.finish_visit(log_data)