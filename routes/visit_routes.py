from fastapi import APIRouter
from services.visit_services import VisitServices
from models.log_model import LogModel
from models.visit_model import VisitModel
from models.vitals_model import VitalsModel
router=APIRouter()
service=VisitServices()

@router.post("/add-visit")
async def add_visit(visit_data:VisitModel):
    return await service.add_visit(visit_data)

@router.post("/add-visit-details.{caregiver_id}")
async def add_visit_details(visit_data:VisitModel):
    return await service.add_visit_details(visit_data)

@router.post("/add-vitals/{patient_id}")
async def add_vitals(vitals_data:VitalsModel):
    return await service.add_vitals(vitals_data)

@router.get("/start-visit/{visit_id}")
async def start_visit(visit_id:str,current_lat:str,current_long:str):
    return await service.start_visit(visit_id,current_lat,current_long)

@router.post("/finish-visit/{visit_id}")
async def finish_visit(log_data:LogModel):
    return await service.finish_visit(log_data)