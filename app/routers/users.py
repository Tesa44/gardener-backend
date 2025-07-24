from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import get_connection
from auth import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from pydantic import BaseModel

router = APIRouter()

class UserIn(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

@router.post("/register")
def register(user: UserIn):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hash_password(user.password)
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s, %s)", (user.name, user.email, hashed))
    conn.commit()
    cursor.close()
    conn.close()
    return {"msg": "User registered"}

@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (user.email,))
    db_user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer", "user": {"name": db_user.get("name", "Unknown")}}

