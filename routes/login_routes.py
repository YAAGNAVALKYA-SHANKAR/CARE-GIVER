from fastapi import APIRouter
from services.login_services import LoginServices
from models.user_model import UserModel
service =LoginServices()
router=APIRouter()
@router.post("/register")
async def register_user(user_data:UserModel):return await service.register_user(user_data)
@router.post("/login")
async def login_user(email:str,password:str):return await service.login_user(email,password)
@router.post("/change-password")
async def change_password(username:str,old_password:str,new_password:str):return await service.change_password(username,old_password,new_password)