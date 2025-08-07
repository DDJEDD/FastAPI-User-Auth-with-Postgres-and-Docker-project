from fastapi import FastAPI
from authorization.login import auth_router
from authorization.register import reg_router
from authorization.users import user_router

app = FastAPI()
app.include_router(reg_router, tags=["register"])
app.include_router(auth_router, tags=["login"])
app.include_router(user_router, tags=["users"])
@app.get("/")
def start():
    return{"go by":  "/docs"}
