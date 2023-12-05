# routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.users import User, UserCreate, DBUser
from database import get_db
from auth import oauth2_scheme, create_access_token, authenticate_user
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = DBUser(username=user.username, phone=user.phone, address=user.address, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/", response_model=list[User])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(DBUser).offset(skip).limit(limit).all()
    return users

@router.get("/users/{id}", response_model=User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{id}", response_model=User)
def update_user(id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == id).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user
