# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace the existing database URL with the correct MySQL connection URL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://matt:bima123!@tst.mysql.database.azure.com/tst?ssl_ca=DigiCertGlobalRootCA.crt.pem"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Now you can use this engine to interact with the database

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)