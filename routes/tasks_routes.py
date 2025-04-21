from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from database.model import User, Task
from utils.functions import gerar_hash, verificar_senha
from utils.auth import criar_token
from database.database import get_session
from sqlmodel import select, insert

router = APIRouter()

class UserSignUp(BaseModel):
    username: str
    password: str

class UserSignIn(BaseModel):
    username: str
    password: str

class TaskModel(BaseModel):
    title: str
    description: str
    id_user: int

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

def create_task(db: Session, task: TaskModel):
    
    new_task = Task(title=task.title, description=task.description, id_user=task.id_user)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return {"message": "Tarefa criada com sucesso"}

@router.post("/sign_up")
def sign_up(user: UserSignUp, db: Session = Depends(get_session)):
    return create_user(db, user)

@router.post("/sign_in")
def sign_in(user: UserSignIn, db: Session = Depends(get_session)):
    user_db = authenticate_user(db, user)
    
    if "error" in user_db:
        return user_db

    token = criar_token({"sub": user.username})
    return {"message": "Login bem sucedido", "access_token": token, "token_type": "bearer"}


@router.post("/add_task")
def add_task(task: TaskModel, db: Session = Depends(get_session)):
    return create_task(db, task)
