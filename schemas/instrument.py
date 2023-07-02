from pydantic import BaseModel, Optional

class Instrument(BaseModel):
    slaveaddress : Optional[int] = None
    instrument_name : str
    port : int
    mode : str
    baudrate : int
    bytesize : int
    parity : str

    class Config:
        schema_extra = {
            "example": {
                "slaveaddress": 1,
                "instrument_name": "itc_650",
                "port": "COM5",
                "mode": "rtu",
                "baudrate": 115200,
                "bytesize": 8,
                "parity" : "None"
            }
        }