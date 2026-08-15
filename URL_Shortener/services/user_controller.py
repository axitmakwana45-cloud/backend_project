from sqlalchemy.orm import Session
from core.security import hash_password,verify_password,create_access_token
from models.user import User
from schemas.user import Userschema,Loginschema,TokenResponse
from fastapi import HTTPException

def create_user(db : Session,user : Userschema):

    existing_user = db.query(User).filter(
    User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=409,detail="email already exist")
    password = user.password
    db_user = User(
    username=user.username,
    email=user.email,
    password=hash_password(password)
    )
    try :
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        db.rollback()
        raise

def login(db : Session,user : Loginschema):

    use = db.query(User).filter(User.email == user.email).first()

    if use is None:

        raise HTTPException(status_code=401,detail= "email or password is invalid")
    password = use.password
    if not verify_password(user.password,use.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    token = create_access_token(
        {
            "__id": str(use.id)
        }
    )

    return {
        "access_token": f"bearer {token}",
        "token_type": "bearer"
    }
    