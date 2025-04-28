import re
from fastapi.exceptions import HTTPException
class Validators:
    @staticmethod
    async def is_valid_id(id_str:str,prefix:str)->bool:
        pattern=rf"^{prefix}_[0-9]{{3}}$"
        result=bool(re.match(pattern,id_str))
        if result:return result
        elif not result:raise HTTPException(status_code=400,detail="Invalid ID!")