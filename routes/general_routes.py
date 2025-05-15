from fastapi import APIRouter,UploadFile,File,Depends
from services.general_services import GeneralServices
from models.general_model import Documentation
from general.security import Security
router=APIRouter()
service=GeneralServices()

@router.post("/add-image-page")
async def add_images(image_data:Documentation,images:list[UploadFile]=File(...),current_user:dict=Depends(Security.get_current_user)):return await service.add_images(image_data,images)

@router.get("/get-images-page")
async def get_images(doc_id:str,current_user:dict=Depends(Security.get_current_user)):return await service.retrieve_images(doc_id)