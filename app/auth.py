from fastapi import APIRouter, HTTPException
from app import schemas
from app.database import db
from passlib.context import CryptContext
from jose import jwt
import random, os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_username(first, last):
    return f"{first.lower()}{last.lower()}{random.randint(1000, 9999)}"


def create_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=30)})  # Token expiration time
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup", response_model=schemas.SignUpResponse)
async def signup(user: schemas.SignUpRequest):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    username = create_username(user.first_name, user.last_name)
    hashed_password = pwd_context.hash(user.password)

    user_dict = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": username,
        "hashed_password": hashed_password
    }

    await db.users.insert_one(user_dict)

    return {
        "status": "created",
        "username": username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

@router.post("/login", response_model=schemas.LoginResponse)
async def login(data: schemas.LoginRequest):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    query = {"$or": [{"email": data.identifier}, {"username": data.identifier}]}
    user = await db.users.find_one(query)

    if not user or not pwd_context.verify(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user["username"]})
    return {"status": "ok", "token": token}