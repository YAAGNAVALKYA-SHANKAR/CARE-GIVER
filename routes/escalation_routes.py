from fastapi import APIRouter, Depends
from services.escalation_services import EscalationService
from models.escalation_model import EscalationModel
from general.security import Security
service= EscalationService()
router = APIRouter()

"""
This module defines the routes for the Escalation API.
It includes the following routes:
- /escalate-case: POST route to escalate a case.
- /get-escalation-list: GET route to get the list of escalations for a caregiver.
- /get-escalation-details: GET route to get the details of a specific escalation.
"""

@router.post("/escalate-case")
async def escalate_case(escalation: EscalationModel,current_user:dict=Depends(Security.get_current_user)):return await service.escalate_case(escalation)
@router.get("/get-escalation-list/{caregiver_id}")
async def get_escalation_list(caregiver_id: str,current_user:dict=Depends(Security.get_current_user)):return await service.get_all_escalations(caregiver_id)
@router.get("/get-escalation-details/{escalation_id}")
async def get_escalation_details(escalation_id: str,caregiver_id:str,current_user:dict=Depends(Security.get_current_user)):return await service.find_escalation(escalation_id,caregiver_id)