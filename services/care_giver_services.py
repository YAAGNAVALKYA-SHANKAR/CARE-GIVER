from fastapi.exceptions import HTTPException 
from collections import OrderedDict
from general.security import Security
from general.database import db,caregivers,patients,visitations

"""
This module defines the services for the Caregiver API.
It includes the following services:
- add_caregiver: Service to add a new caregiver.
- patient_list: Service to get the list of patients assigned to a caregiver.
- my_schedule: Service to get the schedule of a caregiver.
"""

class CareGiverServices:
    @staticmethod
    async def add_caregiver(caregiver_data):
        """
        Adds a new caregiver to the system.
        :param caregiver_data: The data of the caregiver to be added.
        :return: A success message if the caregiver is added successfully.
        :raises HTTPException: If the caregiver already exists or if there is an error adding the caregiver.
        """
        exisiting_caregiver=await caregivers.find_one({"email":caregiver_data.email})
        if exisiting_caregiver:raise HTTPException(status_code=400,detail="Caregiver already exists!")
        counter_doc=await caregivers.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        caregiver_id=f"CG_{counter_value:04d}"
        ordered_data=OrderedDict([("caregiver_id",caregiver_id),*caregiver_data.dict().items()])
        result=await caregivers.insert_one(ordered_data)
        await db.create_collection(caregiver_id)
        await caregivers.update_one({"function":"ID_counter"},{"$inc":{"count":1}})
        if result:raise HTTPException(status_code=200,detail=f"Caregiver {caregiver_id} added successsfully!")
        else:raise HTTPException(status_code=500,detail="Adding Caregiver failed!")
    @staticmethod
    async def patient_list(caregiver_id):
        """
        Gets the list of patients assigned to a caregiver.
        :param caregiver_id: The ID of the caregiver.
        :return: A list of patients assigned to the caregiver.
        :raises HTTPException: If the caregiver ID is invalid or if there are no patients assigned.
        """
        Security.is_valid_id(caregiver_id,prefix="CG")
        patient_cursor=patients.find({"assigned_caregivers":caregiver_id})
        patient_list=await patient_cursor.to_list(length=None)
        if patient_list:
            for patient in patient_list:patient["_id"]=str(patient["_id"])
            return patient_list
        else:raise HTTPException(status_code=404,detail="No patients assigned!")
    @staticmethod
    async def my_schedule(caregiver_id):
        """
        Gets the schedule of a caregiver.
        :param caregiver_id: The ID of the caregiver.
        :return: A list of visitations scheduled for the caregiver.
        :raises HTTPException: If the caregiver ID is invalid or if there are no visitations scheduled.
        """
        Security.is_valid_id(caregiver_id,prefix="CG")
        cursor=visitations.find({"caregiver_id":caregiver_id})
        visits=await cursor.to_list(length=None)
        if visits:
            for visit in visits:
                visit["_id"]=str(visit["_id"])
                patient_id=visit["patient_id"]
                patient_name=await patients.find_one({"patient_id":patient_id})
                visit["patient_name"]=patient_name["name"]
            return visits
        else:raise HTTPException(status_code=404,detail="No visits scheduled!")