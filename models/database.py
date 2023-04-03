from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import Select
from dotenv import load_dotenv
from os import getenv

load_dotenv()

engine = create_engine(getenv('MYSQL'))
db_session = scoped_session(sessionmaker(autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)

def get_session():
    return db_session

def get_select():
    return Select
