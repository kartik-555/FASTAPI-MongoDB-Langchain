from fastapi import APIRouter, HTTPException, status, Depends
import schemas, models
from database import db
from passlib.context import CryptContext
from jose import jwt
import random, string, os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_username(first, last):
    return f"{first.lower()}{last.lower()}{random.randint(1000, 9999)}"

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def store_token(token: str):
    await db.tokens.insert_one({"token": token})

async def is_token_used(token: str) -> bool:
    token_entry = await db.tokens.find_one({"token": token})
    return token_entry is not None

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
    await store_token(token)
    return {"status": "ok", "token": token}