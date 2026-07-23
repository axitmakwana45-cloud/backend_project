from sqlalchemy.orm import Session
from core.security import hash_password,verify_password
from models.user import User
from schemas.user import Userschema
from fastapi import HTTPException

def create_user(db : Session,user : Userschema):

    existing_user = db.query(User).filter(
    User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=409,detail="email already exist")
    db_user = User(
    username=user.username,
    email=user.email,
    password=hash_password(user.password)
    )
    try :
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        db.rollback()
        raise

    