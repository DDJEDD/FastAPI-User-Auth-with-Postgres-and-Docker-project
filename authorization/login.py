from fastapi import APIRouter, HTTPException, Depends, Request, Response, Cookie
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from authorization.func import get_user, SECRET_KEY, decode_access_token, create_access_token
from authorization.schemas import Login
from db.creation import Sessions
from db.database import get_async_session
from authorization.func import verify_password
from fastapi.responses import JSONResponse
auth_router = APIRouter()
@auth_router.post("/login")
async def login(request: Request,response: Response, login: Login,access_token: str = Cookie(None), session: AsyncSession = Depends(get_async_session) ):
    session_id = str(uuid4())
    loggining = login.login
    passwd = login.password
    device_id = request.headers.get('User-Agent')

    check_user = await get_user(loggining, session)
    if check_user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(passwd, check_user.hashed_password):
        raise HTTPException(status_code=400, detail="invalid password")
    try:
        if access_token:
            dec_token = decode_access_token(access_token, SECRET_KEY)
            token_session_id = dec_token.get("session_id")




            query_existing_session = select(Sessions).where(Sessions.session_id == token_session_id)
            result = await session.execute(query_existing_session)
            existing_session = result.scalars().first()

            if existing_session and existing_session.id_user != check_user.id:
                raise HTTPException(status_code=400, detail="You are already logged in on another account")


            query_of_deleting = delete(Sessions).where(Sessions.session_id == token_session_id,
                                                       Sessions.id_user == check_user.id)
            await session.execute(query_of_deleting)
            await session.commit()
            response.delete_cookie(key="access_token", path="/")


    except Exception as e:
        raise HTTPException(status_code=400, detail=f"something went wrong. {e}")


    access_token = create_access_token(user_id=check_user.id, user_agent=device_id, session_id=session_id)
    new_session = Sessions(
        session_id=session_id,
        device_id=device_id,
        id_user=check_user.id,
    )
    session.add(new_session)
    await session.commit()

    response = JSONResponse(content={
        "accessToken": access_token,
        "sessionData": {
            "session_id": new_session.session_id,
            "device_id": new_session.device_id,
            "user_id": new_session.id_user,
        },
    })
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none", path="/",
                        secure=True)
    return response





