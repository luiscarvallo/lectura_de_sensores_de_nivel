from pydantic import BaseModel, Optional

class Controller(BaseModel):
    slaveaddress : Optional[int] = None
    name : str
    port : int
    mode : str
    baudrate : int
    bytesize : int
    parity : str

    class Config:
        schema_extra = {
            "example": {
                "slaveaddress": 1,
                "name": "itc_650",
                "port": "COM5",
                "mode": "rtu",
                "baudrate": 115200,
                "bytesize": 8,
                "parity" : "None"
            }
        }