from config.database import Base
from sqlalchemy import Column, String, Boolean

class User(Base):

    __tablename__ = "users"

    email = Column(String, primary_key = True)
    password = Column(String)
    user_role = Column(String)
    admin = Column(Boolean)
    first_connection = Column(Boolean)
