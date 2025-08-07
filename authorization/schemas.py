from pydantic import BaseModel
class Login(BaseModel):
     login: str
     password: str
class Register(BaseModel):
     login : str
     password: str
     name: str

