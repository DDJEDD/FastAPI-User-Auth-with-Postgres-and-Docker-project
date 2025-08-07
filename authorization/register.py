from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_async_session

from authorization.schemas import Register
from authorization.func import get_user
from authorization.func import hash_password
from db.creation import Users
reg_router = APIRouter()
@reg_router.post("/register")
async def register(register: Register, session: AsyncSession = Depends(get_async_session)):
    login = register.login

    check_reg_login = await get_user(login, session)

    if check_reg_login:
        raise HTTPException(status_code=400, detail="Username already registered")


    hash_passwd = hash_password(register.password)
    user = Users(
        username=register.name,
        login=register.login,
        hashed_password=hash_passwd,
    )
    session.add(user)
    await session.commit()
    return{"msg": "user created succesfully!"}
