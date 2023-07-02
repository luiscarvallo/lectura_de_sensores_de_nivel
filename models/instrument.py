from config.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Float

class Instrument(Base):

    __tablename__ = "instruments"

    slaveaddress = Column(Integer, primary_key = True)
    instrument_name = Column(String)
    port = Column(Integer)
    mode = Column(String)
    baudrate = Column(Integer)
    bytesize = Column(Integer)
    parity = Column(String)