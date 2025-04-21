from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from database.model import User, Task
from utils.functions import gerar_hash, verificar_senha
from database.database import get_session
from sqlmodel import select

router = APIRouter()

class UserSignUp(BaseModel):
    username: str
    password: str

class UserSignIn(BaseModel):
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

def authenticate_user(db: Session, userBaseModel: UserSignIn):
    username = userBaseModel.username
    password = userBaseModel.password

    # Busca o usuário
    statement = select(User).where(User.username == username)
    result = db.exec(statement).first()

    if result:
        if verificar_senha(password, result.password):
            return {"message": "Login bem-sucedido", "user": result.username}
        else:
            return {"error": "Username ou senha incorretos"}
    return {"error": "Username ou senha incorretos"}

@router.post("/sign_up")
def sign_up(user: UserSignUp, db: Session = Depends(get_session)):
    return create_user(db, user)

@router.post("/sign_in")
def sign_in(user: UserSignIn, db: Session = Depends(get_session)):
    return authenticate_user(db, user)

