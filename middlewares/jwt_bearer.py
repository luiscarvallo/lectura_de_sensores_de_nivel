from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
#from utils.jwt_manager import validate_token
from services.user import UserService
from config.database import Session

class MyBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        db = Session()
        current_user = UserService(db).get_current_user(auth.credentials)
        if not current_user:
            raise HTTPException(status_code=403, detail="Las credenciales son inválidas")
