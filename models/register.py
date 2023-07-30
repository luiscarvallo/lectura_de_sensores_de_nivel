from config.database import Base
from sqlalchemy import Column, String, Integer, Float

class Register(Base):

    __tablename__ = "registers"

    id = Column(Integer, primary_key = True)
    register_name = Column(String) # Para los sensores de nivel serían los nombres de tanques.
    meassure = Column(Float)
    meassure_unit = Column(String)