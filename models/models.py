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
    FullName = column_property(sheffprFirstname + " " + sheffprName + " " + sheffprFathername)


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
    FullSpec = column_property(specShifr + " " + specNapravlenie + " - " + specNapravlennost)


class Formstuding(Base):
    __tablename__ = "form_studing"
    IDform_st = mapped_column(Integer, primary_key=True)
    form_stName = mapped_column(String(100), nullable=False)


class Groups(Base):
    __tablename__ = "groups"
    IDgroups = mapped_column(Integer, primary_key=True)
    groupsName = mapped_column(String(10), nullable=False)
    groupsYear = mapped_column(Integer, nullable=False)
    IDform_st = mapped_column(ForeignKey("form_studing.IDform_st"))
    IDspec = mapped_column(ForeignKey("specializations.IDspec"))


class Students(Base):
    __tablename__ = "students"
    IDstudents = mapped_column(Integer, primary_key=True)
    IDgroups = mapped_column(ForeignKey("groups.IDgroups"))
    studentsFirstname = mapped_column(String(255), nullable=False)
    studentsName = mapped_column(String(255), nullable=False)
    studentsFathername = mapped_column(String(255))
    studentsStudbook = mapped_column(Integer, nullable=False)
    studentsPhone = mapped_column(String(12), nullable=False)
    studentsEmail = mapped_column(String(100), nullable=False)
    Login = mapped_column(String(100), nullable=False)
    Pass = mapped_column(String(100), nullable=False)
    FullName = column_property(studentsFirstname + " " + studentsName + " " + studentsFathername)


class Competensions(Base):
    __tablename__ = "competensions"
    IDcompetensions = mapped_column(Integer, primary_key=True)
    IDspec = mapped_column(ForeignKey("specializations.IDspec"))
    competensionsShifr = mapped_column(String(7), nullable=False)
    competensionsFull = mapped_column(String, nullable=False)


class Initiatorsofprojects(Base):
    __tablename__ = "initiatorsofprojects"
    IDinitpr = mapped_column(Integer, primary_key=True)
    IDorg = mapped_column(ForeignKey("organizations.IDorg"))
    initprFirstname = mapped_column(String(255), nullable=False)
    initprName = mapped_column(String(255), nullable=False)
    initprFathername = mapped_column(String(255))
    initprPositions = mapped_column(String(255), nullable=False)
    initprEmail = mapped_column(String(100), nullable=False)
    initprPhone = mapped_column(String(12), nullable=False)
    Login = mapped_column(String(100), nullable=False)
    Pass = mapped_column(String(100), nullable=False)
    FullName = column_property(initprFirstname + " " + initprName + " " + initprFathername)


class PassportOfProjects(Base):
    __tablename__ = "passportofprojects"
    IDpassport = mapped_column(Integer, primary_key=True, autoincrement=True)
    IDinitpr = mapped_column(ForeignKey("initiatorsofprojects.IDinitpr"))
    IDsheffpr = mapped_column(ForeignKey("sheffofprojects.IDsheffpr"))
    passportName = mapped_column(String(255), nullable=False)
    passportProblem = mapped_column(String)
    passportPurpose = mapped_column(String)
    passportTasks = mapped_column(String)
    passportResults = mapped_column(String)
    passportContent = mapped_column(String)
    passportDeadlines = mapped_column(String)
    passportStages = mapped_column(String)
    passportResources = mapped_column(String)
    passportCost = mapped_column(String)
    passportCriteria = mapped_column(String)
    passportFormresults = mapped_column(String)
    passportPattern = mapped_column(String(1000), nullable=False)
    passportFull = mapped_column(String(1000), nullable=False)
    passportSigned = mapped_column(String(1000), nullable=False)


class StadiaOfProjects(Base):
    __tablename__ = "stadiaofprojects"
    IDstadiaofpr = mapped_column(Integer, primary_key=True)
    stadiaofprName = mapped_column(String(255), nullable=False)


class Projects(Base):
    __tablename__ = "projects"
    IDprojects = mapped_column(Integer, primary_key=True)
    IDpassport = mapped_column(ForeignKey("passportofprojects.IDpassport"))
    IDstadiaofpr = mapped_column(ForeignKey("stadiaofprojects.IDstadiaofpr"))
    projectsFull = mapped_column(String(1000))

class RolesOfProjects(Base):
    __tablename__ = 'rolesofprojects'
    IDroles = mapped_column(Integer, primary_key=True)
    IDpassport = mapped_column(ForeignKey("passportofprojects.IDpassport"))
    rolesRole = mapped_column(String(500), nullable=False)
    rolesAmount = mapped_column(Integer, nullable=False)
    rolesFunction = mapped_column(String, nullable=False)
    rolesCost = mapped_column(Integer)
    rolesRequirements = mapped_column(String, nullable=False)

class SpecializationInProjects(Base):
    __tablename__ = 'specializationsinprojects'
    IDspecinpr = mapped_column(Integer, primary_key=True)
    IDroles = mapped_column(ForeignKey("rolesofprojects.IDroles"))
    IDspec = mapped_column(ForeignKey("specializations.IDspec"))

class CompetensionsInProject(Base):
    __tablename__ = 'competensionsinproject'
    IDcompetensionspr = mapped_column(Integer, primary_key=True)
    IDroles = mapped_column(ForeignKey("rolesofprojects.IDroles"))
    IDcompetensions = mapped_column(ForeignKey("competensions.IDcompetensions"))
