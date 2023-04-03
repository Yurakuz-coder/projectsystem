from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Sheffofprojects(Base):
    __tablename__ = "sheffofprojects"
    IDsheffpr = mapped_column(Integer, primary_key=True)
    IDpositions = mapped_column(ForeignKey("positions.IDpositions"))
    sheffprFirstname = mapped_column(String(255), nullable=False)
    sheffprName = mapped_column(String(255))
    sheffprFathername = mapped_column(String(255))
    sheffprPhone = mapped_column(String(12))
    sheffprEmail = mapped_column(String(100))
    Login = mapped_column(String(100), nullable=False)
    Pass = mapped_column(String(100))
    positionName = relationship("Positions", foreign_keys=[IDpositions])


class Positions(Base):
    __tablename__ = "positions"
    IDpositions = mapped_column(Integer, primary_key=True)
    positionsName = mapped_column(String(100), nullable=False)
