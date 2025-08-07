from authorization.func import decode_access_token, SECRET_KEY
from db.creation import Sessions
from fastapi import APIRouter, Cookie, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from db.creation import Users
from db.database import get_async_session
from fastapi.responses import JSONResponse
user_router = APIRouter()

@user_router.get("/get_users")
async def get_user(session: AsyncSession = Depends(get_async_session), ):
    response = await session.execute(select(Users))
    all_users = response.scalars().all()
    users_sessions = []

    for user in all_users:
        rslt = select(Sessions).where(Sessions.id_user == user.id)
        result_sessions = await session.execute(rslt)
        sessions = result_sessions.scalars().all()
        ssons = []
        for sess in sessions:
            ssons.append({
                "session_id": sess.session_id,
                "device_id": sess.device_id,
                "id_user": sess.id_user
            })
        users_sessions.append({
            "id": user.id,
            "username": user.username,
            "login": user.login,
            "hashed_password": user.hashed_password,
            "sessions": ssons
            })
    return users_sessions


@user_router.get("/logout")
async def logout(response: Response, session: AsyncSession = Depends(get_async_session),access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=404, detail="cookie not found or you are not logged in")

    try:
        dec_token = decode_access_token(access_token, SECRET_KEY)
        token_session_id = dec_token.get("session_id")
        stmt = select(Sessions).where(token_session_id == Sessions.session_id)
        res = await session.execute(stmt)
        sess = res.scalars().first()
        await session.delete(sess)
        await session.commit()
        response = JSONResponse(content={"message": "Successfully logged out"})
        response.delete_cookie(key="access_token", path="/")

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"something went wrong ->  {e}" )
