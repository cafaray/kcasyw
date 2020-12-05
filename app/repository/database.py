from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://sysadminkcasyw:sV6loU*vS@localhost:3306/kcasyw"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL    # , connect_args={"check_same_thread": False}   -> just needed in case of use sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()