from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from schemas.user import Userschema,userresponceschema,TokenResponse,Loginschema
from database.db import get_db
from services import user_controller
from core.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix='/user',tags = ['User'])

@router.post("/register",response_model=userresponceschema)
def register(user : Userschema,db : Session =  Depends(get_db)):
    return user_controller.create_user(db,user)

@router.post("/login",response_model=TokenResponse)
def login(user : Loginschema, db : Session = Depends(get_db)):
    return user_controller.login(db,user)

@router.get("/me")
def me(

    current_user: User = Depends(get_current_user)

):

    return current_user