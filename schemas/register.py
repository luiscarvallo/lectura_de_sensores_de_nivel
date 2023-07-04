from pydantic import BaseModel, Optional
import datetime

class Register(BaseModel):
    id : Optional[int] = None
    controller_address : int
    register_name : str
    meassure : float
    meassure_unit : str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "controller_address": 1,
                "register_name": "ÁCIDO NÍTRICO",
                "meassure": 14.55,
                "meassure_unit": "M3",
            }
        }
