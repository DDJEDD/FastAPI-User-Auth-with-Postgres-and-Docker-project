from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()
print("USER:", os.getenv("NAME_OF_USER"))
print("PASSWORD:", os.getenv("PASSWORD_OF_USER"))
print("DBNAME:", os.getenv("DATABASE_NAME"))
user = os.getenv("NAME_OF_USER")
password = os.getenv("PASSWORD_OF_USER")
dbname = os.getenv("DATABASE_NAME")

DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@postgres_db:5432/{dbname}"


engine = create_async_engine(DATABASE_URL)

Base = declarative_base()
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
