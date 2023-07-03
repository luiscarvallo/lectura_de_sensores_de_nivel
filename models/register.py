from config.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey

class Register(Base):

    __tablename__ = "registers"

    id = Column(Integer, primary_key = True)
    date_time = Column(DateTime, server_default=func.now())
    controller_address = Column(Integer, ForeignKey("controllers.slaveaddress"))
    register_name = Column(String) # Para los sensores de nivel serían los nombres de tanques.
    meassure = Column(Float)
    meassure_unit = Column(String)