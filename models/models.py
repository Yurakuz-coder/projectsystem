from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, column_property


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
    positionsName = relationship("Positions", foreign_keys=[IDpositions])


class Positions(Base):
    __tablename__ = "positions"
    IDpositions = mapped_column(Integer, primary_key=True)
    positionsName = mapped_column(String(100), nullable=False)


class Shefforganizations(Base):
    __tablename__ = "shefforganizations"
    IDshefforg = mapped_column(Integer, primary_key=True)
    shefforgFirstname = mapped_column(String(255), nullable=False)
    shefforgName = mapped_column(String(255), nullable=False)
    shefforgFathername = mapped_column(String(255))
    shefforgPositions = mapped_column(String(255), nullable=False)
    shefforgDoc = mapped_column(String(255), nullable=False)
    shefforgEmail = mapped_column(String(100), nullable=False)
    shefforgPhone = mapped_column(String(12), nullable=False)
    Login = mapped_column(String(100), nullable=False)
    Pass = mapped_column(String(100), nullable=False)
    FullName = column_property(shefforgFirstname + " " + shefforgName + " " + shefforgFathername)


class Organizations(Base):
    __tablename__ = "organizations"
    IDorg = mapped_column(Integer, primary_key=True)
    IDshefforg = mapped_column(ForeignKey("shefforganizations.IDshefforg"))
    orgName = mapped_column(String(255), nullable=False)
    orgYuraddress = mapped_column(String(255), nullable=False)
    orgPostaddress = mapped_column(String(255), nullable=False)
    orgEmail = mapped_column(String(100), nullable=False)
    orgPhone = mapped_column(String(12), nullable=False)

class Contracts(Base):
    __tablename__ = "projectsudycontracts"
    IDcontracts = mapped_column(Integer, primary_key=True)
    IDorg = mapped_column(ForeignKey("organizations.IDorg"))
    contractsNumber = mapped_column(Integer, nullable=False)
    contractsStart = mapped_column(Date, nullable=False)
    contractsFinish = mapped_column(Date, nullable=False)
    contractsPattern = mapped_column(String(1000), nullable=False)
    contractsFull = mapped_column(String(1000), nullable=False)
    contractsSigned = mapped_column(String(1000), nullable=False)
    organizations = relationship("Organizations", foreign_keys=[IDorg])


class Specializations(Base):
    __tablename__ = "specializations"
    IDspec = mapped_column(Integer, primary_key=True)
    specShifr = mapped_column(String(20), nullable=False)
    specNapravlenie = mapped_column(String(255), nullable=False)
    specNapravlennost = mapped_column(String(255), nullable=False)
