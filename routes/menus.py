# routes/menus.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.menus import Menu, MenuCreate, DBMenu
from database import get_db
from auth import get_user_power, oauth2_scheme

router = APIRouter(
    prefix='/menus',
    tags=['menus']
)

@router.post("/menus", response_model=Menu)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_user_power)):
    db_menu = DBMenu(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.get("/menus", response_model=list[Menu])
def read_menus(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    menus = db.query(DBMenu).offset(skip).limit(limit).all()
    return menus

@router.get("/menus/{id}", response_model=Menu)
def read_menu(id: int, db: Session = Depends(get_db)):
    menu = db.query(DBMenu).filter(DBMenu.id == id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu

@router.put("/menus/{id}", response_model=Menu)
def update_menu(id: int, menu: MenuCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_user_power)):
    db_menu = db.query(DBMenu).filter(DBMenu.id == id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    for key, value in menu.dict().items():
        setattr(db_menu, key, value)

    db.commit()
    db.refresh(db_menu)
    return db_menu
