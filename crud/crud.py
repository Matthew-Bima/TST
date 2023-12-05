# crud.py
from sqlalchemy.orm import Session
from models.menu import MenuItem, MenuItemBase
from .database import SessionLocal
from typing import List

def create_menu_item(db: Session, menu_item: MenuItem):
    db_menu_item = MenuItem(**menu_item.dict())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item


def get_menu_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(MenuItem).offset(skip).limit(limit).all()

def read_menu_items(db: Session, skip: int = 0, limit: int = 10):
    return get_menu_items(db, skip=skip, limit=limit)