from fastapi.exceptions import HTTPException 
from collections import OrderedDict
from general.security import Security
from general.database import db,patients

class PatientServices:
    @staticmethod
    async def add_patient(patient_data):
        counter_doc=await patients.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        patient_id=f"PAT_{counter_value:03d}"
        ordered_data=OrderedDict([("patient_id",patient_id),*patient_data.dict().items()])
        assigned_caregivers=ordered_data["assigned_caregivers"]
        for caregiver in assigned_caregivers:await Security.is_valid_id(caregiver,prefix="CG")
        result=await patients.insert_one(ordered_data)
        await db.create_collection(patient_id)
        await db[patient_id].insert_one({"function":"schedule","schedule":[]})
        await db[patient_id].insert_one({"function":"vitals","vitals":[]})
        await patients.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
        if result:return HTTPException(status_code=200,detail=f"Patient {patient_id} added successsfully!")
        else:raise HTTPException(status_code=500,detail="Adding Patient failed!")

    @staticmethod
    async def find_patient(patient_id):
        await Security.is_valid_id(patient_id,prefix="PAT")
        patient=await patients.find_one({"patient_id":patient_id})
        patient["_id"]=str(patient["_id"])
        if not patient:raise HTTPException(status_code=404,detail=f"Patient {patient_id} not found!")
        return patient