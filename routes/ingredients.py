# routes/ingredients.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.ingredients import Ingredient, IngredientCreate, DBIngredient
from database import get_db

router = APIRouter(
    prefix='/ingredients',
    tags=['ingredients']
)

@router.post("/ingredients", response_model=Ingredient)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    db_ingredient = DBIngredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

@router.get("/ingredients", response_model=list[Ingredient])
def read_ingredients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ingredients = db.query(DBIngredient).offset(skip).limit(limit).all()
    return ingredients

@router.get("/ingredients/{id}", response_model=Ingredient)
def read_ingredient(id: int, db: Session = Depends(get_db)):
    ingredient = db.query(DBIngredient).filter(DBIngredient.id == id).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.put("/ingredients/{id}", response_model=Ingredient)
def update_ingredient(id: int, ingredient: IngredientCreate, db: Session = Depends(get_db)):
    db_ingredient = db.query(DBIngredient).filter(DBIngredient.id == id).first()
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    for key, value in ingredient.dict().items():
        setattr(db_ingredient, key, value)

    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

@router.put("/ingredients/{id}/quantity", response_model=Ingredient)
def update_ingredient_quantity(id: int, quantity_change: float, db: Session = Depends(get_db)):
    db_ingredient = db.query(DBIngredient).filter(DBIngredient.id == id).first()

    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    # Update the quantity based on the operation (add or subtract)
    new_quantity = db_ingredient.quantity + quantity_change
    db_ingredient.quantity = new_quantity

    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient
