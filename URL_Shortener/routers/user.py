from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from schemas.user import Userschema,userresponceschema
from database.db import get_db
from services import user_controller

router = APIRouter(prefix='/user',tags = ['User'])

@router.post("/register",response_model=userresponceschema)
def register(user : Userschema,db : Session =  Depends(get_db)):
    return user_controller.create_user(db,user)
