from fastapi.exceptions import HTTPException
from collections import OrderedDict
from general.database import visitations,db,caregivers,vitals
from general.security import Security
radius_m=50
class VisitServices:
    @staticmethod
    async def add_visit(visit_data):
        counter_doc=await visitations.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        visit_id=f"VIS_{counter_value:03d}"
        ordered_data=OrderedDict([("visit_id",visit_id),*visit_data.dict().items()])
        assigned_caregiver=ordered_data["caregiver_id"]
        patient=ordered_data["patient_id"]
        Security.is_valid_id(assigned_caregiver,prefix="CG")
        Security.is_valid_id(patient,prefix="PAT")
        existing_caregiver= await caregivers.find_one({"caregiver_id": assigned_caregiver})
        if not existing_caregiver:raise HTTPException(status_code=404,detail=f"Caregiver {assigned_caregiver} does not exist!")
        ordered_data['scheduled_time']=ordered_data['scheduled_time'].isoformat()
        # ordered_data['start_time']=ordered_data['start_time'].isoformat()
        # ordered_data['end_time']=ordered_data['end_time'].isoformat()
        await visitations.insert_one(ordered_data)
        await visitations.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
        raise HTTPException(status_code=200,detail=f"Visit {visit_id} created succesfully!")

    @staticmethod
    async def add_vitals(vital_data):
        counter_doc=await vitals.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        vitals_id=f"VIT_{counter_value:03d}"
        ordered_data=OrderedDict([("vitals_id",vitals_id),*vital_data.dict().items()])
        patient_id=ordered_data['patient_id']
        caregiver_id=ordered_data['caregiver_id']
        Security.is_valid_id(caregiver_id,prefix="CG")
        Security.is_valid_id(patient_id,prefix="PAT")
        exclude=["patient_id","caregiver_id"]
        latest_vitals= {k: v for k, v in ordered_data.items() if k not in exclude}        
        result1=await vitals.insert_one(ordered_data)
        await vitals.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
        result2=await db[patient_id].update_one({"function":"vitals"},{"$set":{"vitals":latest_vitals}})
        if result1 and result2:raise HTTPException(status_code=200,detail=f"Vitals recorded succesfully for patient:{patient_id}")
        else:raise HTTPException(status_code=400,detail="Adding vitals failed!")

    @staticmethod
    async def mark_arrival(visit_id,current_lat,current_long,method):
        Security.is_valid_id(visit_id,prefix="VIS")
        doc=await visitations.find_one({"visit_id":visit_id})
        target_lat=doc["visit_latitude"]
        target_long=doc["visit_longitude"]
        status=doc["visit_status"]
        if status=="PENDING":
            distance_km=await Security.distance_calculator(current_lat,current_long,target_lat,target_long)
            distance_m=distance_km*1000
            if distance_m>=radius_m:raise HTTPException(status_code=403,detail="Too far from visit location.")
            await visitations.update_one({"visit_id":visit_id},{"$set":{"visit_status":"PENDING"}})
            visit_details=await visitations.find_one({"visit_id":visit_id})
            visit_details["_id"]=str(visit_details["_id"])
            return visit_details
        elif status=="FINISHED":raise HTTPException(status_code=400,detail="Visit has been finished.")
        elif status=="PENDING":raise HTTPException(status_code=400,detail="Visit in progress.")
    
    @staticmethod
    async def finish_visit(log_data):
        dict_data=log_data.model_dump()
        visit_id=dict_data["visit_id"]
        caregiver_id=log_data["caregiver_id"]
        patient_id=log_data["patient_id"]
        Security.is_valid_id(caregiver_id,prefix="CG")
        Security.is_valid_id(patient_id,prefix="PAT")
        Security.is_valid_id(visit_id,prefix="VIS")
        status_doc=await visitations.find_one({"visit_id":visit_id})
        status=status_doc["visit_status"]
        if status=="IN PROGRESS":await visitations.update_one({"visit_id":visit_id},{"$set":{"visit_status":"FINISHED"}})
        elif status=="FINISHED":raise HTTPException(status_code=400,detail="Visit already completed.")
        elif status=="PENDING":raise HTTPException(status_code=400,detail="Visit not started.")

    @staticmethod
    async def add_visit_details(visit_data):
        caregiver_id=visit_data["caregiver_id"]
        patient_id=visit_data["patient_id"]
        Security.is_valid_id(caregiver_id,prefix="CG")
        Security.is_valid_id(patient_id,prefix="PAT")
        await db[patient_id].insert_one(visit_data)