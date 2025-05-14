from fastapi import APIRouter,Depends,HTTPException
from services.login_services import LoginServices
from models.user_model import UserModel,SignupModel
from general.security import Security
service =LoginServices()
router=APIRouter()

"""
This module defines the routes for the Login API.
It includes the following routes:
- /signup: POST route to signup a new user.
- /login: POST route to log in a user.
- /change-password: POST route to change a user's password.
- /forgot-password: POST route to send a password reset email.
- /reset-password: POST route to reset a user's password.
"""

@router.post("/signup")
async def signup_user(user_data:SignupModel):return await service.signup_user(user_data)
@router.post("/login")
async def login_user(email:str,password:str):return await service.login_user(email,password)
@router.post("/change-password")
async def change_password(username:str,old_password:str,new_password:str,current_user:dict=Depends(Security.get_current_user)):return await service.change_password(username,old_password,new_password)
@router.post("/forgot-password")
async def forgot_password(email:str):return await service.forgot_password(email)
@router.post("/reset-password")
async def reset_password(token: str, new_password: str):return await service.reset_password(token, new_password)
