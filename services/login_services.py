from datetime import datetime,timedelta
from fastapi import HTTPException
from collections import OrderedDict
from models.user_model import UserModel
from general.database import registered_users,caregivers
from general.security import Security
MAX_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=15
class LoginServices:
    @staticmethod
    async def login_user(email:str,password:str):
        user=await registered_users.find_one({"email":email})
        if not user:return{"success":False,"message":"User not found."}
        if user.get("is_locked"):
            lock_time=user.get("lockout_time")
            if lock_time and(datetime.utcnow()-lock_time).total_seconds()<LOCKOUT_DURATION_MINUTES*60:return{"success":False,"message":"Account locked. Try again later."}
            else:await registered_users.update_one({"email":email},{"$set":{"is_locked":False,"failed_attempts":0,"lockout_time":None}})
        if not Security.verify_password(password, user["password"]):
            new_failed_count=user.get("failed_attempts",0)+1
            update_fields={"failed_attempts":new_failed_count,"last_failed_attempt":datetime.utcnow()}
            if new_failed_count>=MAX_ATTEMPTS:
                update_fields["is_locked"]=True
                update_fields["lockout_time"]=datetime.utcnow()
            await registered_users.update_one({"email":email},{"$set":update_fields})
            return{"success":False,"message":"Invalid password."}
        access_token=Security.create_access_token(data={"sub": user["username"]},expires_delta=timedelta(minutes=60))
        user["access_token"]=access_token
        await registered_users.update_one({"email":email},{"$set":{"failed_attempts":0,"is_locked":False,"lockout_time":None}})
        user.pop("_id",None)
        user.pop("password",None)
        user.pop("is_active",None)
        user.pop("user_id",None)
        user.pop("failed_attempts",None)
        user.pop("is_locked",None)
        return {"success":True,"message":"Login successful.","user_details":user}
    @staticmethod
    async def register_user(user_data:UserModel):
        exisitng_caregiver=await caregivers.find_one({"email":user_data.email})
        if not exisitng_caregiver:raise HTTPException(status_code=400,detail="Email is not registered!")
        existing_user1=await registered_users.find_one({"username":user_data.username})
        if existing_user1:return{"success":False,"message":"Username already exists."}
        existing_user2=await registered_users.find_one({"email":user_data.email})
        if existing_user2:return{"success":False,"message":"Email already exists."}
        counter_doc=await registered_users.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        user_id=f"USER_{counter_value:04d}"
        await registered_users.update_one({"function":"ID_counter"},{"$inc":{"count":1}})
        hashed_password=Security.hash_password(user_data.password)        
        user_dict=user_data.dict()
        user_dict["password"]=hashed_password
        user_dict["user_id"]=user_id
        user_dict=OrderedDict([("user_id",user_id),*user_dict.items()])
        await registered_users.insert_one(user_dict)
        return {"success":True,"message":"User registered successfully."}
    @staticmethod
    async def change_password(username:str,old_password:str,new_password:str):
        user=await registered_users.find_one({"username":username})
        if not user:return{"success":False,"message":"User not found."}
        if not Security.verify_password(old_password,user["password"]):return{"success":False,"message":"Old password is incorrect."}
        hashed_new_password=Security.hash_password(new_password)
        await registered_users.update_one({"username":username},{"$set":{"password":hashed_new_password}})
        return {"success":True,"message":"Password changed successfully."}