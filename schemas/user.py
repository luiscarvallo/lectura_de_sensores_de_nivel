from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    user_role: str
    admin: bool
    first_connection: bool

    class Config:
        schema_extra = {
            "example": {
                "username": "user",
                "password": "12345",
                "user_role": "Ingeniero de Procesos",
                "admin": False,
                "first_connection": True
            }
        }