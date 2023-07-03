import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_db_name = "../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{ps.path.join(base_dir, sqlite_db_name)}"

engine = create_engine(database_url, echo=True)

Session = sessionmaker(bin=engine)

Base = declarative_base()