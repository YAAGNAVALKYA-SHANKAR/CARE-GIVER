from fastapi import HTTPException
from general.database import db, nursing

class NursingServices:
    @staticmethod
    async def add_nursing_task(nursing_data):
        service = {"id":nursing_data.id,
            "description": nursing_data.description}
        result = await nursing.insert_one(service)
        if result:
            return {"message": f"Nursing service '{nursing_data.id}' added successfully!"}
        else:
            raise HTTPException(status_code=500, detail="Adding nursing service failed!")
    @staticmethod
    async def get_nursing_tasks(id):
        task_details=await nursing.find_one({"id": id})
        if not task_details:
            raise HTTPException(status_code=404, detail=f"Nursing task with ID {id} not found!")
        task_details["_id"]=str(task_details["_id"])
        task_details.pop("_id",None)
        return task_details
    
