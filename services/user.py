from schemas.user import User
from models.user import User as UserModel
from jwt_manager import create_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi.exceptions import HTTPException
from utils.pw_manager import verify_password

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class UserService():
    def __init__(self, db) -> None:
        self.db = db

    def get_user(self, username: str):
        result = self.db.query(UserModel).filter(UserModel.email == username).first()
        return result

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username=username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    def login(self, form: OAuth2PasswordRequestForm = Depends()):
        result = self.search_user(form.username)
        
        if not result:
            raise HTTPException(status_code=400, detail="El email no es correcto")

        if not username.password == result.password:
            raise HTTPException(status_code=400, detail="La contraseña no es correcta")
        
        token: str = create_token(user.dict())
        
        return token
            


    def create_user(self, user: User) -> None:
        new_user = UserModel(**user.dict())

        self.db.add(new_register)
        self.db.commit()

        return

    async def current_user(token: str = Depends(oauth2)):
        token