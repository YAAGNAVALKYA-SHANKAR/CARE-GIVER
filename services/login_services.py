from datetime import datetime
from fastapi import HTTPException
from collections import OrderedDict
from models.user_model import UserModel
from general.database import users,caregivers
from general.security import Security

MAX_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

class LoginServices:

    @staticmethod
    async def login_user(email: str, password: str):
        user = await users.find_one({"email": email})
        if not user:
            return {"success": False, "message": "User not found."}

        # Check if account is locked
        if user.get("is_locked"):
            lock_time = user.get("lockout_time")
            if lock_time and (datetime.utcnow() - lock_time).total_seconds() < LOCKOUT_DURATION_MINUTES * 60:
                return {"success": False, "message": "Account locked. Try again later."}
            else:
                # Unlock the user after cooldown
                await users.update_one({"email": email}, {"$set": {"is_locked": False, "failed_attempts": 0, "lockout_time": None}})
        
        # Password verification
        if not await Security.verify_password(password, user["password"]):
            new_failed_count = user.get("failed_attempts", 0) + 1
            update_fields = {
                "failed_attempts": new_failed_count,
                "last_failed_attempt": datetime.utcnow()
            }

            if new_failed_count >= MAX_ATTEMPTS:
                update_fields["is_locked"] = True
                update_fields["lockout_time"] = datetime.utcnow()

            await users.update_one(
                {"email": email},
                {"$set": update_fields}
            )

            return {"success": False, "message": "Invalid password."}

        # Reset failure counters on successful login
        await users.update_one(
            {"email": email},
            {"$set": {"failed_attempts": 0, "is_locked": False, "lockout_time": None}}
        )

        # Remove sensitive data
        user.pop("_id", None)
        user.pop("password", None)
        user.pop("is_active", None)
        user.pop("role", None)
        user.pop("user_id", None)

        return {"success": True, "message": "Login successful.", "user_details": user}

    @staticmethod
    async def register_user(user_data:UserModel):
        exisitng_caregiver=await caregivers.find_one({"email":user_data.email})
        if not exisitng_caregiver:raise HTTPException(status_code=400,detail="Caregiver does not exist!")
        existing_user = await users.find_one({"username": user_data.username})
        if existing_user:
            return {"success": False, "message": "Username already exists."}
        counter_doc=await users.find_one({"function": "ID_counter"})
        counter_value=counter_doc["count"]
        user_id=f"USER_{counter_value:04d}"
        await users.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)

        hashed_password = await Security.hash_password(user_data.password)        
        user_dict = user_data.dict()
        user_dict["password"] = hashed_password
        user_dict["user_id"] = user_id
        user_dict = OrderedDict([("user_id", user_id), *user_dict.items()])

        await users.insert_one(user_dict)
        return {"success": True, "message": "User registered successfully."}

    @staticmethod
    async def change_password(username: str, old_password: str, new_password: str):
        user = await users.find_one({"username": username})
        if not user:
            return {"success": False, "message": "User not found."}

        if not await Security.verify_password(old_password, user["password"]):
            return {"success": False, "message": "Old password is incorrect."}

        hashed_new_password = await Security.hash_password(new_password)
        await users.update_one(
            {"username": username},
            {"$set": {"password":hashed_new_password}}
        )

        return {"success": True, "message": "Password changed successfully."}
