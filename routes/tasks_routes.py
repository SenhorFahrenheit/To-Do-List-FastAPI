from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, select
from database.model import Task
from database.database import get_session
from utils.auth import verificar_token
from typing import Optional



router = APIRouter()

class TaskModel(BaseModel):
    title: str
    description: str
    id_user: int

class TaskUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

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
    return JSONResponse(content=[task.model_dump() for task in tasks], status_code=200)

def remove_task(db: Session, token, task_id):
    user_id = int(token["sub"])
    statement = select(Task).where(Task.id_user == user_id, Task.id == task_id)
    task = db.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada ou não pertence ao usuário")

    db.delete(task)
    db.commit()

    message = {"message": "Tarefa excluída com sucesso"}

    return message

def update_task(db: Session, token, task_id, taskupdate: TaskUpdateModel):
    user_id = int(token['sub'])
    statement = select(Task).where(Task.id_user == user_id, Task.id == task_id)
    task = db.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada ou não pertence ao usuário")
    
    if taskupdate.title is not None:
        task.title = taskupdate.title
    if taskupdate.description is not None:
        task.description = taskupdate.description

    db.commit()
    db.refresh(task)

    return {"message": "Tarefa atualizada com sucesso"}

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

@router.delete("/tasks/{task_id}")
def delete_tasks(
    task_id: int,
    db: Session = Depends(get_session),
    token_valid: str = Depends(verificar_token)
):
    if token_valid is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")     


    return remove_task(db, token_valid, task_id)

@router.put("/tasks/{task_id}")
def put_tasks(
    taskupdate: TaskUpdateModel,
    task_id: int,
    db: Session = Depends(get_session),
    token_valid: str = Depends(verificar_token)
   
):
    if token_valid is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")     


    return update_task(db, token_valid, task_id, taskupdate)