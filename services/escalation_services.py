from fastapi import HTTPException
from general.security import Security
from general.database import escalations
from models.escalation_model import EscalationModel 

"""
This module defines the services for the Escalation API.
It includes the following services:
- escalate_case: Service to handle the escalation of a case.
- find_escalation: Service to find an escalation by its ID and caregiver ID.
- get_all_escalations: Service to get all escalations for a specific caregiver.
"""

class EscalationService:
    @staticmethod
    async def escalate_case(escalation:EscalationModel):
        """
        Service method to handle the escalation of a case.
        :param escalation: The escalation data to be added.
        :return: A success message if the escalation is added successfully.
        :raises HTTPException: If the escalation already exists or if there is an error adding the escalation.
        """
        Security.is_valid_id(escalation.patient_id,prefix="PAT")
        Security.is_valid_id(escalation.caregiver_id,prefix="CG")
        Security.is_valid_id(escalation.visit_id,prefix="VIS")
        dict_data = escalation.dict()
        result = await escalations.find_one({"patient_id": escalation.patient_id, "visit_id": escalation.visit_id})
        if result:
            raise HTTPException(status_code=400, detail="Escalation already exists for this patient and visit.")
        counter_doc = await escalations.find_one({"function": "ID_counter"})
        counter_value = counter_doc["count"] if counter_doc else 1
        escalation_id = f"ESC_{counter_value:04d}"
        dict_data["escalation_id"] = escalation_id
        result = await escalations.insert_one(dict_data)
        if result:
            return {"success": True, "message": "Escalation added successfully.","Escalation ID:":escalation_id}
        elif Exception:
            raise HTTPException(status_code=500, detail=f"Failed to add escalation.{Exception}")
        
    @staticmethod
    async def find_escalation(escalation_id:str, caregiver_id:str):
        """
        Service method to find an escalation by its ID and caregiver ID.
        :param escalation_id: The ID of the escalation.
        :param caregiver_id: The ID of the caregiver.
        :return: The escalation data if found.
        :raises HTTPException: If the escalation is not found.
        """
        Security.is_valid_id(escalation_id,prefix="ESC")
        Security.is_valid_id(caregiver_id,prefix="CG")
        result = await escalations.find_one({"escalation_id": escalation_id, "caregiver_id": caregiver_id})
        if result:
            result["_id"] = str(result["_id"])
            return result
        else:
            raise HTTPException(status_code=404, detail="Escalation not found.")
        
    @staticmethod
    async def get_all_escalations(caregiver_id:str):
        """
        Service method to get all escalations for a specific caregiver.
        :param caregiver_id: The ID of the caregiver.
        :return: A list of escalations for the caregiver.
        :raises HTTPException: If the caregiver ID is invalid or if there are no escalations found.
        """
        Security.is_valid_id(caregiver_id,prefix="CG")
        cursor = escalations.find({"caregiver_id": caregiver_id})
        escalations_list = await cursor.to_list(length=None)
        if escalations_list:
            for escalation in escalations_list:
                escalation["_id"] = str(escalation["_id"])
            return escalations_list
        else:
            raise HTTPException(status_code=404, detail="No escalations found.")
        