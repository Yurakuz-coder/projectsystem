from sqlalchemy import *

class sheffofprojects (Base):
    __table__ = Table('sheffofprojects', metadata, autoload=True)


class positions (Base):
    __table__ = Table('positions', metadata, autoload=True)