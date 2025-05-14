import re
from jose import JWTError,jwt
from datetime import datetime,timedelta
from math import radians,cos,sin,asin,sqrt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
"""
This module provides security-related functions for the application, including:
- JWT token creation and verification
- Password hashing and verification
- ID validation
- Distance calculation between two geographical points
- Password reset token creation and verification
- User authentication and authorization
"""
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
SECRET_KEY="99cd77130576c415193ccf3eca16a1ed76adfb5e69a84551909d0ec0d4298f1d"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/Home-Care/Login/login")
"""
OAuth2PasswordBearer is a class that provides a way to extract the token from the request
and pass it to the dependency function. It expects the token to be in the "Authorization" header format
"""
class Security:
    def get_current_user(token:str=Depends(oauth2_scheme)):
        """
        This function decodes the JWT token and retrieves the username from it.
        If the token is invalid or expired, it raises an HTTPException with a 401 status code.
        """
        try:
            payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            username=payload.get("sub")
            if username is None:raise HTTPException(status_code=401, detail="Invalid token payload.")
            return {"username": username}
        except JWTError:raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")
    def verify_access_token(token:str):
        """
        This function verifies the JWT token and returns the payload if valid.
        If the token is invalid or expired, it returns None.
        """
        try:
            payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            return payload
        except JWTError:return None
    def create_access_token(data:dict,expires_delta:timedelta=None):
        """
        This function creates a JWT token with the given data and expiration time.
        If no expiration time is provided, it defaults to 60 minutes.
        """
        to_encode=data.copy()
        expire=datetime.utcnow()+(expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp":expire})
        print(f"Token data:{to_encode}")
        return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    def is_valid_id(id_str:str,prefix:str)->bool:
        """
        This function checks if the given ID string matches the expected format.
        The format is defined as a prefix followed by an underscore and three digits.
        """
        pattern=rf"^{prefix}_[0-9]{{3}}$"
        result=bool(re.match(pattern,id_str))
        if result:return result
        elif not result:raise HTTPException(status_code=400,detail="Invalid ID!")
    def distance_calculator(current_lat,current_long,target_lat,target_long):
        """ 
        Calculate the distance between two geographical points using the Haversine formula.
        Returns:
        float: Distance in kilometers between the two points.
        """
        R=6371.0
        lat1_rad,lon1_rad,lat2_rad,lon2_rad=map(radians,[current_lat,current_long,target_lat,target_long])
        dlat=lat2_rad-lat1_rad
        dlon=lon2_rad-lon1_rad
        a=sin(dlat/2)**2+cos(lat1_rad)*cos(lat2_rad)*sin(dlon/2)**2
        c=2*asin(sqrt(a))
        distance_km=R*c
        return distance_km
    def hash_password(password:str)->str:
        """
        Hash a password using bcrypt algorithm.
        """
        return pwd_context.hash(password)
    def verify_password(plain_password:str,hashed_password: str)->bool:
        """ 
        Verify a password against its hashed version.
        """
        return pwd_context.verify(plain_password, hashed_password)
    def create_reset_token(email: str):
        """
        Create a password reset token for the given email.
        The token is valid for 5 minutes.
        """
        expire = datetime.utcnow() + timedelta(minutes=5)
        payload = {"sub": email, "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)    
    def verify_reset_token(token: str):
        """
        Verify the password reset token.
        If valid, return the email address from the token.
        If invalid or expired, return None.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub")  # email
        except:
            return None