from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from databases.database import get_db
from models.users import DBUser
import bcrypt

# Replace these with your actual Google OAuth credentials
GOOGLE_CLIENT_ID = "349293765740-mqnmmavfk6o0kmhuh64jbkkg1r6ij2lp.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:8000/login/callback"  # Replace with your actual callback URL

# Create an instance of OAuth2AuthorizationCodeBearer
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="token",
    authorizationUrl=f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=email profile",
)


SECRET_KEY = "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"  # Change this with your actual secret key
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "role": data.get("role")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to authenticate a user
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

# Function to verify a password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")  # Include role in the token payload
        if username is None or role is None:
            raise credentials_exception
        token_data = {"sub": username, "role": role}
    except JWTError:
        raise credentials_exception
    return token_data

def get_user_power(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ("staff", "superadmin"):
        raise HTTPException(status_code=403, detail="You do not have access to this resource")
    return current_user
