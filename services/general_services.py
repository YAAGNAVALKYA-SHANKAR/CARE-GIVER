import base64
from fastapi import UploadFile, File,HTTPException
from models.general_model import Documentation
from general.database import documents
from general.security import Security
class GeneralServices:
    @staticmethod
    async def add_images(images_data:Documentation,uploaded_images:list[UploadFile]=File(...)):
        Security.is_valid_id(images_data.visit_id,prefix="VIS")
        dict_data = images_data.dict()
        counter_doc=await documents.find_one({"function": "ID_counter"})
        counter_value=counter_doc["count"] if counter_doc else 1
        doc_id=f"DOC_{counter_value:04d}"
        dict_data["doc_id"]=doc_id
        inserted_count=0
        docs=[]
        for image in uploaded_images:
            bytes_image=await image.read()
            base64_image=base64.b64encode(bytes_image).decode("utf-8")
            docs.append(base64_image)
            inserted_count+=1
        dict_data["images"]=docs
        result=await documents.insert_one(dict_data)
        if result.inserted_id:return{"success":True,"message":f"{inserted_count} documents added successfully","doc_id":doc_id}
        else: raise HTTPException(status_code=400,detail="Document insertion failed")

    @staticmethod
    async def retrieve_images(doc_id):
        Security.is_valid_id(doc_id,prefix="DOC")
        doc=await documents.find_one({"doc_id":doc_id})
        if not doc:raise HTTPException(status_code=404,detail="Document not found")
        doc.pop("_id",None)
        return {"success":True,"message":"Document fetched successfully","document":doc}