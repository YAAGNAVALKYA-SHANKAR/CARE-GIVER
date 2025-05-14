import smtplib
from email.mime.text import MIMEText
from datetime import datetime,timedelta
from fastapi import HTTPException
from models.user_model import UserModel
from general.database import registered_users,caregivers
from general.security import Security
MAX_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=15

"""
This module defines the services for the Login API.
It includes the following services:
- login_user: Service to log in a user.
- register_user: Service to register a new user.
- change_password: Service to change a user's password.
- forgot_password: Service to send a password reset email.
- reset_password: Service to reset a user's password.
"""

class LoginServices:
    @staticmethod
    async def login_user(email:str,password:str):
        """
        This function handles user login.
        It checks if the user exists, verifies the password,
        and handles account lockout after multiple failed attempts.
        :param email: The email of the user.
        :param password: The password of the user.
        :return: A success message if login is successful, otherwise an error message.
        """
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
    async def signup_user(user_data:UserModel):
        """
        This function handles user registration.
        It checks if the user already exists, and if not,
        it creates a new user with a hashed password.
        :param user_data: The data of the user to be registered.
        :return: A success message if registration is successful, otherwise an error message.
        """
        exisiting_caregiver=await caregivers.find_one({"email":user_data.email})
        if not exisiting_caregiver:raise HTTPException(status_code=400,detail="Email is not registered!")
        existing_user=await registered_users.find_one({"email":user_data.email})
        if existing_user:return{"success":False,"message":"User already exists."}
        counter_doc=await registered_users.find_one({"function":"ID_counter"})
        counter_value=counter_doc["count"]if counter_doc else 1
        user_id=f"USER_{counter_value:04d}"
        await registered_users.update_one({"function":"ID_counter"},{"$inc":{"count":1}})
        hashed_password=Security.hash_password(user_data.password)
        user_dict={}
        user_dict["user_id"]=user_id        
        user_dict["password"]=hashed_password    
        user_dict["email"]=user_data.email  
        await registered_users.insert_one(user_dict)
        return {"success":True,"message":"User registered successfully."}
    @staticmethod
    async def change_password(username:str,old_password:str,new_password:str):
        """
        This function handles password change for a user.
        It checks if the user exists, verifies the old password,
        and updates the password if the old password is correct.
        :param username: The username of the user.
        :param old_password: The old password of the user.
        :param new_password: The new password to be set.
        :return: A success message if password change is successful, otherwise an error message.
        """
        user=await registered_users.find_one({"username":username})
        if not user:return{"success":False,"message":"User not found."}
        if not Security.verify_password(old_password,user["password"]):return{"success":False,"message":"Old password is incorrect."}
        hashed_new_password=Security.hash_password(new_password)
        await registered_users.update_one({"username":username},{"$set":{"password":hashed_new_password}})
        return {"success":True,"message":"Password changed successfully."}
    
    @staticmethod
    async def forgot_password(email:str):
        """
        This function handles password reset request.
        It checks if the user exists, generates a reset token,
        and sends a password reset email to the user.
        :param email: The email of the user.
        :return: A success message if the email is sent successfully, otherwise an error message.
        """
        user=await registered_users.find_one({"email":email})
        if not user:return{"success":False,"message":"User not found."}
        reset_token=Security.create_reset_token(email)
        LoginServices.send_reset_email(email, reset_token)        
        return {"success":True,"message":"Password reset link sent to your email."}
    
    @staticmethod
    async def send_reset_email(to_email: str, token: str):
        """
        This function sends a password reset email to the user.
        :param to_email: The email of the user.
        :param token: The reset token to be included in the email.
        :return: A success message if the email is sent successfully, otherwise an error message
        """
        reset_link = f"http://your-frontend.com/reset-password?token={token}"
        body = f"Click this link to reset your password: {reset_link}"
        msg = MIMEText(body)
        msg["Subject"] = "Password Reset Request"
        msg["From"] = "noreply@yourapp.com"
        msg["To"] = to_email
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("your-email@gmail.com", "your-password")
            smtp.send_message(msg)
        return {"success":True,"message":"Password reset email sent."}

    @staticmethod
    async def reset_password(token: str, new_password: str):
        """
        This function handles password reset.
        It verifies the reset token, checks if the user exists,
        and updates the password if the token is valid.
        :param token: The reset token sent to the user.
        :param new_password: The new password to be set.
        :return: A success message if password reset is successful, otherwise an error message.
        """
        email = Security.verify_reset_token(token)
        if not email:return{"success":False,"message":"Invalid or expired token."}
        hashed_new_password=Security.hash_password(new_password)
        await registered_users.update_one({"email":email},{"$set":{"password":hashed_new_password}})
        return {"success":True,"message":"Password reset successfully."}