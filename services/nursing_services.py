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
        cursor= nursing.find({"id": id})
        tasks = []
        async for task in cursor:
            task["_id"]=str(task["_id"])
            task.pop("_id",None)
            task.pop("id",None)
            tasks.append(task)
        if not tasks:   
            raise HTTPException(status_code=404, detail=f"Nursing task with ID {id} not found!")
        return tasks
        # task_details=await nursing.find_one({"id": id})
        # if not task_details:
        #     raise HTTPException(status_code=404, detail=f"Nursing task with ID {id} not found!")
        # task_details["_id"]=str(task_details["_id"])
        # task_details.pop("_id",None)
        # return task_details
    
