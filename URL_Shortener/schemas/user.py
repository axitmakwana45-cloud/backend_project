from pydantic import BaseModel, EmailStr
from datetime import datetime

class Userschema(BaseModel):

    username: str

    email: EmailStr

    password: str

class userresponceschema(BaseModel):

    id : int

    username : str

    email : EmailStr

    created_at : datetime


class Loginschema(BaseModel):

    email:EmailStr

    password:str