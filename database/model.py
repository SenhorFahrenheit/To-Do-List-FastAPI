from typing import Optional
from sqlmodel import SQLModel, Field

# Modelo de usuário, representando a tabela "user" no banco de dados
class User(SQLModel, table=True):
    # ID do usuário (chave primária, autoincrementável)
    id: Optional[int] = Field(default=None, primary_key=True)
    # Nome de usuário
    username: str
    # Senha do usuário (armazenada em formato hash)
    password: str

# Modelo de tarefa, representando a tabela "task" no banco de dados
class Task(SQLModel, table=True):
    # ID da tarefa (chave primária, autoincrementável)
    id: Optional[int] = Field(default=None, primary_key=True)
    # Título da tarefa
    title: str
    # Descrição da tarefa (opcional)
    description: Optional[str] = None
    # ID do usuário associado à tarefa (chave estrangeira referenciando a tabela "user")
    id_user: int = Field(foreign_key="user.id")
