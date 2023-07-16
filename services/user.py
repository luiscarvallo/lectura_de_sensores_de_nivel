from schemas.user import User
from models.user import User as UserModel
from jwt_manager import create_token

class UserService():
    def __init__(self, db) -> None:
        self.db = db

    def login(self, user: User):
        result = self.db.query(UserModel).filter(UserModel.email == user.email).first()
        if user.password == result.password:
            token: str = create_token(user.dict())
            return token

    def create_user(self, user: User) -> None:
        new_user = UserModel(**user.dict())

        self.db.add(new_register)
        self.db.commit()

        return