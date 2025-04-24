from fastapi.exceptions import HTTPException 
from general.database import db, caregivers
from collections import OrderedDict

class CareGiverServices:
    @staticmethod
    async def add_caregiver(caregiver_data):
        counter_doc=await caregivers.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        caregiver_id=f"CG_{counter_value:03d}"
        ordered_data=OrderedDict([("caregiver_id",caregiver_id),*caregiver_data.dict().items()])
        result=await caregivers.insert_one(ordered_data)
        await db.create_collection(caregiver_id)
        await db[caregiver_id].insert_one({"function":"Schedule","Schedule":[]})
        await caregivers.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
        if result:return HTTPException(status_code=200,detail=f"Caregiver {caregiver_id} added successsfully!")
        else:raise HTTPException(status_code=500,detail="Adding Caregiver failed!")