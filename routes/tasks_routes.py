from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from database.model import User, Task
from utils.functions import gerar_hash
from database.database import get_session


router = APIRouter()

class UserSignUp(BaseModel):
    username: str
    password: str


def create_user(db: Session, userBaseModel: UserSignUp):
    username = userBaseModel.username
    password_hash = gerar_hash(userBaseModel.password)
    user = User(username=username, password=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/sign_up")
def sign_up(user: UserSignUp, db: Session = Depends(get_session)):
    return create_user(db, user)

