from fastapi import APIRouter
from services.visit_services import VisitServices
from models import log_model,visit_model,vitals_model
router=APIRouter()
service=VisitServices()

@router.post("/add-visit")
async def add_visit(visit_data:visit_model.VisitModel):
    return await service.add_visit(visit_data)

@router.post("/add-visit-details.{caregiver_id}")
async def add_visit_details():
    return

@router.post("/add-vitals/{patient_id}")
async def add_vitals(vitals_data:vitals_model.VitalsModel):
    return await service.add_vitals(vitals_data)

@router.post("/finish-visit/{visit_id}")
async def finish_visit(log_data:log_model.LogModel):
    return await service.finish_visit(log_data)