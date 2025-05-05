from fastapi.exceptions import HTTPException 
from collections import OrderedDict
from general.security import Security
from general.database import db,caregivers,patients,visitations
class CareGiverServices:
    @staticmethod
    async def add_caregiver(caregiver_data):
        counter_doc=await caregivers.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        caregiver_id=f"CG_{counter_value:03d}"
        ordered_data=OrderedDict([("caregiver_id",caregiver_id),*caregiver_data.dict().items()])
        result=await caregivers.insert_one(ordered_data)
        await db.create_collection(caregiver_id)
        await caregivers.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
        if result:raise HTTPException(status_code=200,detail=f"Caregiver {caregiver_id} added successsfully!")
        else:raise HTTPException(status_code=500,detail="Adding Caregiver failed!")
    @staticmethod
    async def patient_list(caregiver_id):
        Security.is_valid_id(caregiver_id,prefix="CG")
        patient_cursor=patients.find({"assigned_caregivers":caregiver_id})
        patient_list=await patient_cursor.to_list(length=None)
        if patient_list:
            for patient in patient_list:patient["_id"]=str(patient["_id"])
            return patient_list
        else:raise HTTPException(status_code=404,detail="No patients assigned!")
    @staticmethod
    async def my_schedule(caregiver_id):
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