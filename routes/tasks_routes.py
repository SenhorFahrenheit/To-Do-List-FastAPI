from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, select
from database.model import Task
from database.database import get_session
from utils.auth import verificar_token
from typing import Optional

router = APIRouter()

# Modelo para criação de tarefa, com os campos obrigatórios.
class TaskModel(BaseModel):
    title: str  # Título da tarefa
    description: str  # Descrição da tarefa

# Modelo para atualização de tarefa, com campos opcionais.
class TaskUpdateModel(BaseModel):
    title: Optional[str] = None  # Novo título da tarefa (opcional)
    description: Optional[str] = None  # Nova descrição da tarefa (opcional)

# Função para criar uma nova tarefa no banco de dados.
def create_task(db: Session, task: TaskModel, user_id: int):
    new_task = Task(
        title=task.title,
        description=task.description,
        id_user=user_id  # A tarefa estará associada a um usuário
    )
    db.add(new_task)
    db.commit()  # Confirma a inserção da tarefa no banco
    db.refresh(new_task)  # Atualiza o objeto para refletir os dados persistidos
    
    return {"message": "Tarefa criada com sucesso"}

# Função para recuperar as tarefas de um usuário específico.
def get_tasks(db: Session, token):
    user_id = int(token['sub'])  # Obtém o ID do usuário do token
    statement = select(Task).where(Task.id_user == user_id)  # Consulta as tarefas do usuário
    tasks = db.exec(statement).all()  # Executa a consulta e obtém as tarefas
    
    # Mesmo sem tarefas, retorne lista vazia com status 200
    return JSONResponse(content=[task.model_dump() for task in tasks], status_code=200)

# Função para remover uma tarefa do banco de dados.
def remove_task(db: Session, token, task_id):
    user_id = int(token["sub"])  # Obtém o ID do usuário do token
    statement = select(Task).where(Task.id_user == user_id, Task.id == task_id)  # Verifica se a tarefa pertence ao usuário
    task = db.exec(statement).first()  # Executa a consulta e obtém a tarefa

    # Caso a tarefa não seja encontrada ou não pertença ao usuário, lança erro 404
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada ou não pertence ao usuário")

    db.delete(task)  # Exclui a tarefa do banco de dados
    db.commit()  # Confirma a exclusão

    message = {"message": "Tarefa excluída com sucesso"}

    return message

# Função para atualizar uma tarefa no banco de dados.
def update_task(db: Session, token, task_id, taskupdate: TaskUpdateModel):
    user_id = int(token['sub'])  # Obtém o ID do usuário do token
    statement = select(Task).where(Task.id_user == user_id, Task.id == task_id)  # Verifica se a tarefa pertence ao usuário
    task = db.exec(statement).first()  # Executa a consulta e obtém a tarefa

    # Caso a tarefa não seja encontrada ou não pertença ao usuário, lança erro 404
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada ou não pertence ao usuário")
    
    # Atualiza os campos da tarefa, caso os valores sejam fornecidos
    if taskupdate.title is not None:
        task.title = taskupdate.title
    if taskupdate.description is not None:
        task.description = taskupdate.description

    db.commit()  # Confirma a atualização
    db.refresh(task)  # Atualiza o objeto para refletir os dados persistidos

    return {"message": "Tarefa atualizada com sucesso"}

# Rota para criar uma nova tarefa
@router.post("/add_task")
def add_task(
    task: TaskModel,  # Dados da tarefa a ser criada
    db: Session = Depends(get_session),  # Obtém a sessão do banco de dados
    token_valid: str = Depends(verificar_token)  # Valida o token de autenticação
):
    # Verifica se o token é válido
    if token_valid is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")
    
    user_id = int(token_valid["sub"])  # Obtém o ID do usuário do token
    return create_task(db, task, user_id)  # Cria a tarefa no banco

# Rota para listar todas as tarefas de um usuário
@router.get("/list_tasks")
def list_tasks(
    db: Session = Depends(get_session),  # Obtém a sessão do banco de dados
    token_valid: str = Depends(verificar_token)  # Valida o token de autenticação
):
    # Verifica se o token é válido
    if token_valid is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")
    
    return get_tasks(db, token_valid)  # Recupera as tarefas do banco

# Rota para excluir uma tarefa
@router.delete("/tasks/{task_id}")
def delete_tasks(
    task_id: int,  # ID da tarefa a ser excluída
    db: Session = Depends(get_session),  # Obtém a sessão do banco de dados
    token_valid: str = Depends(verificar_token)  # Valida o token de autenticação
):
    # Verifica se o token é válido
    if token_valid is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")     

    return remove_task(db, token_valid, task_id)  # Exclui a tarefa do banco

# Rota para atualizar uma tarefa
@router.put("/tasks/{task_id}")
def put_tasks(
    taskupdate: TaskUpdateModel,  # Dados para atualização da tarefa
    task_id: int,  # ID da tarefa a ser atualizada
    db: Session = Depends(get_session),  # Obtém a sessão do banco de dados
    token_valid: str = Depends(verificar_token)  # Valida o token de autenticação
):
    # Verifica se o token é válido
    if token_valid is None:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")     

    return update_task(db, token_valid, task_id, taskupdate)  # Atualiza a tarefa no banco
