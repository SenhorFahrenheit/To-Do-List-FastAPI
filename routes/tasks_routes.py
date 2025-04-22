from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
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

@router.post("/add_task")
def add_task(
    task: TaskModel,
    db: Session = Depends(get_session),
    token_valid: str = Depends(verificar_token)
):
    if token_valid is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")
    
    return create_task(db, task)
