from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from db.creation import Users, Sessions
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
def verify_password(unhashed_password: str, hashed_password: str):
    return pwd_context.verify(unhashed_password, hashed_password)
async def get_user(login: str, session:AsyncSession):
    response = await session.execute(select(Users).where(Users.login == login))
    user = response.scalars().first()
    return user
def hash_password(password: str):
    return pwd_context.hash(password)
def create_access_token(user_id: int, user_agent: str, session_id: str):
    to_encode = {
        "user_id": user_id,
        "user_agent": user_agent,
        "session_id": session_id,
        }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def decode_access_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")