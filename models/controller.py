from config.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Float

class Controller(Base):

    __tablename__ = "controllers"

    id = Column(Integer, primary_key = True)
    host = Column(String)
    port = Column(Integer)