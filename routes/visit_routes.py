from fastapi import APIRouter
from services.visit_services import VisitServices
from models.visit_model import VisitModel

router=APIRouter()
service=VisitServices()

@router.post("/add-visit")
async def add_visit(visit_data:VisitModel):
    return await service.add_visit(visit_data)