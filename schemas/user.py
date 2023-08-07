from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str
    user_role: str
    admin: bool
    disabled: bool