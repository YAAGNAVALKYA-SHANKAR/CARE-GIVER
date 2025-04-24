from fastapi.exceptions import HTTPException
from collections import OrderedDict
from general.database import visitations,db,caregivers

class VisitServices:
    @staticmethod
    async def add_visit(visit_data):
        counter_doc=await visitations.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        visit_id=f"VIS_{counter_value:03d}"
        visit_details={}
        ordered_data=OrderedDict([("visit_id",visit_id),*visit_data.dict().items()])
        assigned_caregiver=ordered_data["caregiver_id"]
        existing_caregiver= await caregivers.find_one({"caregiver_id": assigned_caregiver})
        if not existing_caregiver:raise HTTPException(status_code=404,detail=f"Caregiver {assigned_caregiver} does not exist!")
        ordered_data['scheduled_time']=ordered_data['scheduled_time'].isoformat()
        ordered_data['start_time']=ordered_data['start_time'].isoformat()
        ordered_data['end_time']=ordered_data['end_time'].isoformat()
        await visitations.insert_one(ordered_data)
        await visitations.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
        visit_details['time']=ordered_data['scheduled_time']
        visit_details['patient']=ordered_data['patient_id']
        result=await db[assigned_caregiver].update_one({"function":"Schedule"},{"$set":{"schedule":visit_details}})
        if result:raise HTTPException(status_code=200,detail=f"Visit {visit_id} created succesfully!")
        else:raise HTTPException(status_code=400,detail="Visit creation failed!")        