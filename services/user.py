from schemas.user import User
from schemas.token import TokenData
from models.user import User as UserModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, Form
from fastapi.exceptions import HTTPException
from utils.pw_manager import verify_password, get_password_hash
from datetime import timedelta
from utils.jwt_manager import create_access_token
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "07f271739b7c58bac3ae1f410c2832ea7c743e17876fba9c907ea0200f77adef"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

    def create_user(self, username: str, user_role: str) -> None:
        
        user = self.get_user(username=username)

        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya ha sido registrado")

        pw = 12345
        hashed_password = get_password_hash(password=pw)
        new_user = UserModel(email=username, password=hashed_password, user_role=user_role, admin=False, first_connection=True)

        self.db.add(new_user)
        self.db.commit()

        return    
    
    def create_first_user(self, username: str, password: str, user_role: str, admin: bool, first_connection: bool) -> None:
        
        user = self.get_user(username=username)

        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya ha sido registrado")

        hashed_password = get_password_hash(password=password)
        new_user = UserModel(email=username, password=hashed_password, user_role=user_role, admin=admin, first_connection=first_connection)

        self.db.add(new_user)
        self.db.commit()

        return

    def change_password(self, token: Annotated[str, Depends(oauth2_scheme)], password: str, confirm_password: str) -> None:

        if password != confirm_password:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Las contraseñas no coinciden")

        current_user = self.get_current_user(token=token)

        current_user.password = get_password_hash(password=password)
        current_user.first_connection = False

        return


    def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        
        user = self.get_user(username=token_data.username)

        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(self, 
        current_user: Annotated[User, Depends(get_current_user)]
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    def login_for_access_token(self, form_data):
        user = self.authenticate_user(form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return access_token

    def verify_admin(self, token: Annotated[str, Depends(oauth2_scheme)]):
        current_user = self.get_current_user(token=token)

        if not current_user.admin:
            raise HTTPException(status_code=400, detail="Not admin")
        return current_user

    def read_users_me(self, 
        current_user: Annotated[User, Depends(get_current_active_user)]
    ):
        return current_user

    def modify_user(self, username: str, user: User):
        result = self.get_user(username=username)

        result.email = user.email
        result.password = get_password_hash(password=user.password)
        result.user_role = user.user_role
        result.admin = user.admin
        result.disabled = user.disabled

        self.db.commit()
        
        return

    def delete_user(self, username: str):
        result = self.get_user(username=username)

        self.db.delete(result)
        self.db.commit()

        return

