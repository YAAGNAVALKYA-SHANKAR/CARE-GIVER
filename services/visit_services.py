import base64
from fastapi.exceptions import HTTPException
from collections import OrderedDict
from general.database import visitations,db,caregivers,vitals,patients,documents
from general.security import Security
from models.visit_model import SummaryModel
from models.log_model import LogModel

radius_m=50
class VisitServices:
    @staticmethod
    async def add_visit(visit_data):
        counter_doc=await visitations.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        visit_id=f"VIS_{counter_value:04d}"
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
        await visitations.update_one({"function":"ID_counter"},{"$inc":{"count":1}})
        raise HTTPException(status_code=200,detail=f"Visit {visit_id} created succesfully!")

    @staticmethod
    async def add_vitals(vital_data):
        counter_doc=await vitals.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        vitals_id=f"VIT_{counter_value:04d}"
        ordered_data=OrderedDict([("vitals_id",vitals_id),*vital_data.dict().items()])
        patient_id=ordered_data['patient_id']
        caregiver_id=ordered_data['caregiver_id']
        Security.is_valid_id(caregiver_id,prefix="CG")
        Security.is_valid_id(patient_id,prefix="PAT")
        exclude=["patient_id","caregiver_id"]
        latest_vitals= {k: v for k, v in ordered_data.items() if k not in exclude}        
        result1=await vitals.insert_one(ordered_data)
        await vitals.update_one({"function":"ID_counter"},{"$inc":{"count":1}})
        result2=await db[patient_id].update_one({"function":"vitals"},{"$set":{"vitals":latest_vitals}})
        if result1 and result2:return {"success":True,"message":f"Vitals recorded succesfully for patient:{patient_id}","Vitals":vitals_id}
        else:raise HTTPException(status_code=400,detail="Adding vitals failed!")

    @staticmethod
    async def mark_arrival(visit_id,current_lat,current_long,selfie):
        Security.is_valid_id(visit_id,prefix="VIS")
        doc=await visitations.find_one({"visit_id":visit_id})
        target_lat=doc["visit_latitude"]
        target_long=doc["visit_longitude"]
        status=doc["visit_status"]       
        if status=="FINISHED":raise HTTPException(status_code=400,detail="Visit has already been finished.")
        else:
            distance_km=await Security.distance_calculator(current_lat,current_long,target_lat,target_long)
            distance_m=distance_km*1000
            if distance_m>=radius_m:raise HTTPException(status_code=403,detail=f"Too far from visit location. Distance:{distance_m}")
            selfie_bytes = await selfie.read()
            selfie_base64 = base64.b64encode(selfie_bytes).decode("utf-8")
            await visitations.update_one({"visit_id":visit_id},{"$set":{"selfie_on_arrival":selfie_base64}})
            return {"success":True,"message":"Arrival marked successfully.","distance":distance_m}

    @staticmethod
    async def start_visit(visit_id):
        Security.is_valid_id(visit_id,prefix="VIS")
        doc=await visitations.find_one({"visit_id":visit_id})
        status=doc["visit_status"]
        if status=="NOT STARTED":
            visit_details={}
            patient_id=doc["patient_id"]
            await visitations.update_one({"visit_id":visit_id},{"$set":{"visit_status":"IN PROGRESS"}})
            await db[patient_id].insert_one({"function":"visit","details":doc})
            doc.pop("_id")
            visit_details["visit details"]=doc      
            patient_details=await patients.find_one({"patient_id":patient_id})
            patient_details.pop("_id")
            visit_details["patient details"]=patient_details
            return {"success":True,"message":"Visit started successfully.","visit details":visit_details}
        elif status=="IN PROGRESS":raise HTTPException(status_code=400,detail="Visit already started.")
        elif status=="FINISHED":raise HTTPException(status_code=400,detail="Visit has already been finished.")
    
    @staticmethod
    async def finish_visit(log_data:LogModel):
        dict_data=log_data.model_dump()
        Security.is_valid_id(log_data.caregiver_id,prefix="CG")
        Security.is_valid_id(log_data.patient_id,prefix="PAT")
        Security.is_valid_id(log_data.visit_id,prefix="VIS")
        Security.is_valid_id(log_data.vitals_id,prefix="VIT")
        status_doc=await visitations.find_one({"visit_id":log_data.visit_id})
        vital_snapshot=await vitals.find_one({"vitals_id":log_data.vitals_id})
        status_doc.pop("_id")
        vital_snapshot.pop("_id")
        notes=log_data.clinical_notes
        return_details={}
        return_details["vitals snapshot"]=vital_snapshot
        return_details["visit details"]=status_doc
        return_details["clinical notes"]=notes
        status=status_doc["visit_status"]
        if status=="IN PROGRESS":
            await visitations.update_one({"visit_id":log_data.visit_id},{"$set":{"visit_status":"FINISHED"}})
            await db[log_data.patient_id].update_one({"function":"visit"},{"$set":{"visit":log_data}})
            return {"success":True,"message":"Visit finished successfully.","details":return_details}
        else:return {"success":False,"message":"Visit is not started or is finished already."}

    @staticmethod
    async def add_visit_details(visit_data,visit_id):
        caregiver_id=visit_data["caregiver_id"]
        patient_id=visit_data["patient_id"]
        Security.is_valid_id(visit_id,prefix="VIS")
        Security.is_valid_id(caregiver_id,prefix="CG")
        Security.is_valid_id(patient_id,prefix="PAT")
        visit_data["visit_id"]=visit_id
        await db[patient_id].insert_one(visit_data)
        await db[caregiver_id].insert_one(visit_data)
        return {"success":True,"message":f"Visit details for {visit_id}"}

    @staticmethod
    async def view_summary(summary_data:SummaryModel):
        Security.is_valid_id(summary_data.visit_id,prefix="VIS")
        Security.is_valid_id(summary_data.vitals_id,prefix="VIT")
        Security.is_valid_id(summary_data.doc_id,prefix="DOC")
        Security.is_valid_id(summary_data.patient_id,prefix="PAT")
        summary_details={}
        patient_info=patients.find_one({"patient_id":summary_data.patient_id})
        patient_info.pop("_id",None)
        summary_details["Patient Info"]=patient_info
        vital_snapshot=vitals.find_one({"vitals_id":summary_data.vitals_id})
        vital_snapshot.pop("_id",None)
        summary_details["Vitals Snapshot"]=vital_snapshot
        visit_details=visitations.find_one({"visit_id":summary_data.visit_id})
        visit_details.pop("_id",None)
        summary_details["Visit Details"]=visit_details
        documentations=documents.find_one({"doc_id":summary_data.doc_id})
        documentations.pop("_id",None)
        summary_details["Documentation"]=documentations
        if not patient_info:raise HTTPException(status_code=404,detail="Patient details not found.")
        if not vital_snapshot:raise HTTPException(status_code=404,detail="Patient vitals details not found.")
        if not visit_details:raise HTTPException(status_code=404,detail="Visit details not found.")
        if not documentations:raise HTTPException(status_code=404,detail="Patient documentation details not found.")
        return {"success":False,"message":"Visit summary fetched successully","visit summary":summary_details}