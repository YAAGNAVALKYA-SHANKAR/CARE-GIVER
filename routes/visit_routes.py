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
async def add_visit_details():
    return

@router.post("/add-vitals/{patient_id}")
async def add_vitals(vitals_data:VitalsModel):
    return await service.add_vitals(vitals_data)

@router.post("/finish-visit/{visit_id}")
async def finish_visit(log_data:LogModel):
    return await service.finish_visit(log_data)