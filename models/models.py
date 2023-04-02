from sqlalchemy import *

class sheffofprojects (Base):
    __table__ = Table('sheffofprojects', metadata, autoload=True)