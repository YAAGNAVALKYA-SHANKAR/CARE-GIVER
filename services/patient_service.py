from fastapi.exceptions import HTTPException 
from collections import OrderedDict
from general.security import Security
from general.database import db,patients

"""
This module defines the services for the Patient API.
It includes the following services:
- add_patient: Service to add a new patient.
- find_patient: Service to find a patient by their ID.
"""
class PatientServices:
    @staticmethod
    async def add_patient(patient_data):
        """
        Adds a new patient to the system.
        :param patient_data: The data of the patient to be added.
        :return: A success message if the patient is added successfully.
        :raises HTTPException: If the patient already exists or if there is an error adding the patient.
        """
        counter_doc=await patients.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        patient_id=f"PAT_{counter_value:04d}"
        ordered_data=OrderedDict([("patient_id",patient_id),*patient_data.dict().items()])
        assigned_caregivers=ordered_data["assigned_caregivers"]
        for caregiver in assigned_caregivers:Security.is_valid_id(caregiver,prefix="CG")
        result=await patients.insert_one(ordered_data)
        await db.create_collection(patient_id)
        await db[patient_id].insert_one({"function":"schedule","schedule":[]})
        await db[patient_id].insert_one({"function":"vitals","vitals":[]})
        await patients.update_one({"function":"ID_counter"},{"$inc":{"count":1}})
        if result:return HTTPException(status_code=200,detail=f"Patient {patient_id} added successsfully!")
        else:raise HTTPException(status_code=500,detail="Adding Patient failed!")

    @staticmethod
    async def find_patient(patient_id):
        """
        Finds a patient by their ID.
        :param patient_id: The ID of the patient to be found.
        :return: The patient data if found.
        """
        Security.is_valid_id(patient_id,prefix="PAT")
        patient=await patients.find_one({"patient_id":patient_id})
        patient["_id"]=str(patient["_id"])
        if not patient:raise HTTPException(status_code=404,detail=f"Patient {patient_id} not found!")
        return patient