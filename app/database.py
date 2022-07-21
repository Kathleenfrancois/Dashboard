from sqlalchemy import create engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://pguser:pgpass@postgresql:5432/pgdb"

engine = create engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker (autocommit=False ,autoflush=False, bind=engine)

Base = declarative_base()
