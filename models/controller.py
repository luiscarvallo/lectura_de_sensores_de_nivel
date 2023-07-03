from config.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Float

class Controller(Base):

    __tablename__ = "controllers"

    slaveaddress = Column(Integer, primary_key = True)
    name = Column(String)
    port = Column(Integer)
    mode = Column(String)
    baudrate = Column(Integer)
    bytesize = Column(Integer)
    parity = Column(String)