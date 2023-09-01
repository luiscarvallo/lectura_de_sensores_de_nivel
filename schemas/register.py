from pydantic import BaseModel
import datetime

class Register(BaseModel):
    id : int
    register_name : str
    meassure : float
    meassure_unit : str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "register_name": "ÁCIDO NÍTRICO",
                "meassure": 14.55,
                "meassure_unit": "kg",
            }
        }
