from fastapi.exceptions import HTTPException 
from general.database import db, patients
from collections import OrderedDict

class PatientServices:
    @staticmethod
    async def add_patient(patient_data):
        counter_doc=await patients.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        patient_id=f"PAT_{counter_value:03d}"
        ordered_data=OrderedDict([("patient_id",patient_id),*patient_data.dict().items()])
        result=await patients.insert_one(ordered_data)
        await db.create_collection(patient_id)
        await db[patient_id].insert_one({"function":"Schedule","Schedule":[]})
        await patients.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
        if result:return HTTPException(status_code=200,detail=f"Patient {patient_id} added successsfully!")
        else:raise HTTPException(status_code=500,detail="Adding Patient failed!")