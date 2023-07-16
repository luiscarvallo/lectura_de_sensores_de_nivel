from config.database import Base
from sqlalchemy import Column, String

class User(Base):

    __tablename__ = "users"

    email = Column(String, primary_key = True)
    password = Column(String)