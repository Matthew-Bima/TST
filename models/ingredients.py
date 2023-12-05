# models/ingredient.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from database import Base

class IngredientBase(BaseModel):
    name: str
    category: str
    description: str
    quantity: float
    unit: str

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True

# SQLAlchemy model
class DBIngredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    description = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    
    menus = relationship("DBMenu", secondary="menu_ingredient_association", back_populates="ingredients")
