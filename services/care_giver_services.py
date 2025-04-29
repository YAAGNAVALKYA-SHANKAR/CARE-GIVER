from fastapi.exceptions import HTTPException 
from collections import OrderedDict
from general.validators import Validators
from general.database import db,caregivers,patients

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
        if result:return HTTPException(status_code=200,detail=f"Caregiver {caregiver_id} added successsfully!")
        else:raise HTTPException(status_code=500,detail="Adding Caregiver failed!")

    @staticmethod
    async def patient_list(caregiver_id):
        result=await Validators.is_valid_id(caregiver_id,prefix="CG")
        if result:
            patient_cursor=patients.find({"assigned_caregivers":caregiver_id})
            patient_list=await patient_cursor.to_list(length=None)
            if patient_list:
                for patient in patient_list:patient["_id"]=str(patient["_id"])
                return patient_list
            else:raise HTTPException(status_code=404,detail="No patients assigned!")

    @staticmethod
    async def my_schedule(caregiver_id):
        await Validators.is_valid_id(caregiver_id,prefix="CG")
        schedule=await db[caregiver_id].find_one({"function":"schedule"})
        if not schedule:raise HTTPException(status_code=404,detail="No schedule document found!")
        schedule_details=schedule["schedule"]
        if schedule_details:return schedule_details
        else:raise HTTPException(status_code=400,detail="Nothing Scheduled!")