# models/menu.py
from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class MenuIngredientAssociation(Base):
    __tablename__ = 'menu_ingredient_association'
    menu_id = Column(Integer, ForeignKey('menus.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantity = Column(Float)
    
class MenuBase(BaseModel):
    name: str
    category: str
    description: str
    price: float
    ingredients: List[int] = []

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: int
    ingredients: List[int] = []

    class Config:
        orm_mode = True

# SQLAlchemy model
class DBMenu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    description = Column(String)
    price = Column(Float)
    
    ingredients = relationship("DBIngredient", secondary="menu_ingredient_association", back_populates="menus")
