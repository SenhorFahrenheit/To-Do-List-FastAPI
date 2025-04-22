from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, select
from database.model import Task
from database.database import get_session
from utils.auth import verificar_token

router = APIRouter()

class TaskModel(BaseModel):
    title: str
    description: str
    id_user: int



def create_task(db: Session, task: TaskModel):
    new_task = Task(
        title=task.title,
        description=task.description,
        id_user=task.id_user
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return {"message": "Tarefa criada com sucesso"}

def get_tasks(db: Session, token):
    user_id = int(token['sub'])
    statement = select(Task).where(Task.id_user == user_id)
    tasks = db.exec(statement).all()
    # Mesmo sem tarefas, retorne lista vazia com status 200
    return JSONResponse(content=tasks, status_code=200)

@router.post("/add_task")
def add_task(
    task: TaskModel,
    db: Session = Depends(get_session),
    token_valid: str = Depends(verificar_token)
):
    print(token_valid)
    if token_valid is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")
    
    return create_task(db, task)

@router.get("/list_tasks")
def list_tasks(
    db: Session = Depends(get_session),
    token_valid: str = Depends(verificar_token)
):
    if token_valid is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")
    
    return get_tasks(db, token_valid)