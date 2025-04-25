from fastapi.exceptions import HTTPException
from collections import OrderedDict
from general.database import visitations,db,caregivers,patients,logs,vitals
from general.id_validator import Validators

class VisitServices:
    @staticmethod
    async def add_visit(visit_data):
        counter_doc=await visitations.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        visit_id=f"VIS_{counter_value:03d}"
        visit_details={}
        ordered_data=OrderedDict([("visit_id",visit_id),*visit_data.dict().items()])
        assigned_caregiver=ordered_data["caregiver_id"]
        patient=ordered_data["patient_id"]
        valid_cg_id=await Validators.is_valid_id(assigned_caregiver,prefix="CG")
        valid_pat_id=await Validators.is_valid_id(patient,prefix="PAT")
        if valid_cg_id and valid_pat_id:
            existing_caregiver= await caregivers.find_one({"caregiver_id": assigned_caregiver})
            if not existing_caregiver:raise HTTPException(status_code=404,detail=f"Caregiver {assigned_caregiver} does not exist!")
            ordered_data['scheduled_time']=ordered_data['scheduled_time'].isoformat()
            ordered_data['start_time']=ordered_data['start_time'].isoformat()
            ordered_data['end_time']=ordered_data['end_time'].isoformat()
            await visitations.insert_one(ordered_data)
            await visitations.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
            visit_details['time']=ordered_data['scheduled_time']
            visit_details['patient']=ordered_data['patient_id']
            result1=await db[assigned_caregiver].update_one({"function":"schedule"},{"$set":{"schedule":visit_details}})
            result2=await db[patient].update_one({"function":"schedule"},{"$set":{"schedule":visit_details}})
            if result1 and result2:raise HTTPException(status_code=200,detail=f"Visit {visit_id} created succesfully!")
            else:raise HTTPException(status_code=400,detail="Visit creation failed!")

    @staticmethod
    async def add_vitals(vital_data):
        counter_doc=await vitals.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        vitals_id=f"VIT_{counter_value:03d}"
        ordered_data=OrderedDict([("vitals_id",vitals_id),*vital_data.dict().items()])
        patient_id=ordered_data['patient_id']
        caregiver_id=ordered_data['caregiver_id']
        valid_cg_id=await Validators.is_valid_id(caregiver_id,prefix="CG")
        valid_pat_id=await Validators.is_valid_id(patient_id,prefix="PAT")
        exclude=["patient_id","caregiver_id"]
        latest_vitals= {k: v for k, v in ordered_data.items() if k not in exclude}
        if valid_cg_id and valid_pat_id:
            result1=await logs.insert_one(ordered_data)
            await logs.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
            result2=await db[patient_id].update_one({"function":"vitals"},{"$set":{"vitals":latest_vitals}})
            if result1 and result2:raise HTTPException(status_code=200,detail=f"Vitals recorded succesfully for patient:{patient_id}")
            else:raise HTTPException(status_code=400,detail="Adding vitals failed!")

    @staticmethod
    async def finish_visit(log_data):
        return 0

    @staticmethod
    async def add_visit_details(visit_data):
        caregiver_id=visit_data["caregiver_id"]
        patient_id=visit_data["patient_id"]
        valid_cg_id=await Validators.is_valid_id(caregiver_id,prefix="CG")
        valid_pat_id=await Validators.is_valid_id(patient_id,prefix="PAT")
        if valid_cg_id and valid_pat_id:
            await db[patient_id].insert_one(visit_data)