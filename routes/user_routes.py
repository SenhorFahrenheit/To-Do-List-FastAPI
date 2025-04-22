from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from database.model import User
from utils.functions import gerar_hash, verificar_senha
from utils.auth import criar_token
from database.database import get_session

router = APIRouter()

# Modelos para requisição de cadastro e login de usuários
class UserSignUp(BaseModel):
    username: str
    password: str

class UserSignIn(BaseModel):
    username: str
    password: str

# Função para criar um novo usuário
def create_user(db: Session, userBaseModel: UserSignUp):
    username = userBaseModel.username

    # Verifica se o nome de usuário já existe
    statement = select(User).where(User.username == username)
    result = db.exec(statement).first()
    if result:
        raise HTTPException(status_code=400, detail="Este username já está em uso")

    # Criptografa a senha e salva o usuário no banco
    password_hash = gerar_hash(userBaseModel.password)
    user = User(username=username, password=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Cadastro feito com sucesso", "Bem vindo: ": user}

# Função para autenticar o usuário
def authenticate_user(db: Session, userBaseModel: UserSignIn):
    username = userBaseModel.username
    password = userBaseModel.password

    # Verifica se o nome de usuário e senha estão corretos
    statement = select(User).where(User.username == username)
    result = db.exec(statement).first()
    if result and verificar_senha(password, result.password):
        return {"message": "Login bem-sucedido", "user": result.username, "user id": result.id}
    
    # Lança erro caso as credenciais sejam inválidas
    raise HTTPException(status_code=401, detail="Username ou senha incorretos")

# Rota para cadastro de usuário (POST /sign_up)
@router.post("/sign_up")
def sign_up(user: UserSignUp, db: Session = Depends(get_session)):
    return create_user(db, user)

# Rota para login de usuário (POST /sign_in)
@router.post("/sign_in")
def sign_in(user: UserSignIn, db: Session = Depends(get_session)):
    user_db = authenticate_user(db, user)
    
    # Gera token JWT para login bem-sucedido
    token = criar_token({"sub": str(user_db["user id"])})
    return {"message": "Login bem sucedido", "access_token": token, "token_type": "bearer"}
