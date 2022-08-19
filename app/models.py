from sqlalchemy import Column, Float, String, Integer, Numeric
from .database import Base
class salary(Base):
    __tablename__ = "salary"
    id = Column(Integer, primary_key=True, index=True)
    player = Column(String, unique=True, index=True)
    positions = Column(String)
    team = Column(String)
    salary= Column(Numeric)

class Project(Base):
    __tablename__ = "Project"
    id = Column(Integer, primary_key=True, index=True)
    state= Column(String, unique=True, index=True)
    total = Column(Numeric)
    hom = Column(Numeric)
    sui = Column(Numeric)
    ranks= Column(Numeric)
