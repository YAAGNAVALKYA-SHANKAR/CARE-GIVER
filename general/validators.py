import re
from math import radians, cos, sin, asin, sqrt
from fastapi.exceptions import HTTPException
class Validators:
    @staticmethod
    async def is_valid_id(id_str:str,prefix:str)->bool:
        pattern=rf"^{prefix}_[0-9]{{3}}$"
        result=bool(re.match(pattern,id_str))
        if result:return result
        elif not result:raise HTTPException(status_code=400,detail="Invalid ID!")

    @staticmethod
    async def distance_calculator(current_lat,current_long,target_lat,target_long):
        R=6371.0
        lat1_rad,lon1_rad,lat2_rad,lon2_rad=map(radians,[current_lat,current_long,target_lat,target_long])
        dlat=lat2_rad-lat1_rad
        dlon=lon2_rad-lon1_rad
        a=sin(dlat/2)**2+cos(lat1_rad)*cos(lat2_rad)*sin(dlon/2)**2
        c=2*asin(sqrt(a))
        distance_km=R*c
        return distance_km
