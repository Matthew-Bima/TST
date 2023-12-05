from enum import Enum
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from database import Base
import bcrypt

class UserRole(str, Enum):
    member = "member"
    staff = "staff"
    superadmin = "superadmin"

class UserBase(BaseModel):
    username: str
    phone: str
    address: str

class UserCreate(UserBase):
    password: str 
    role: UserRole

class User(UserBase):
    id: int
    role: UserRole
    hashed_password: str
    
    class Config:
        orm_mode = True

# SQLAlchemy model
class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    address = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # New field for storing hashed password
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
