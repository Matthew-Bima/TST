from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from routes import menus, users, ingredients
from fastapi.responses import JSONResponse


# Create FastAPI app instance
app = FastAPI()
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


# CORS (Cross-Origin Resource Sharing) settings to allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes from menu.py
app.include_router(menus.router)
app.include_router(users.router)
app.include_router(ingredients.router)