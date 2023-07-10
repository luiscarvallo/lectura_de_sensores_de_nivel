from pydantic import BaseModel

class Controller(BaseModel):
    id: int
    host: str
    port: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "host": "192.168.0.200",
                "port": 8899,
            }
        }