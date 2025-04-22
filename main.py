# Importando as dependências do FastAPI e de outros módulos
from fastapi import FastAPI
from database.database import create_db_and_tables  # Função para criar o banco e tabelas no início
from contextlib import asynccontextmanager  # Utilizado para criar um contexto assíncrono (lifespan) para a app
from routes.tasks_routes import router as task_routes  # Importando as rotas de tarefas
from routes.user_routes import router as user_routes  # Importando as rotas de usuários

# Definindo o lifespan da aplicação (o ciclo de vida da app)
# Esse contexto é usado para ações que precisam ser feitas na inicialização da aplicação, como criação do banco
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Chamando a função que cria o banco de dados e as tabelas necessárias ao iniciar o app
    create_db_and_tables()
    yield  # O yield é um ponto de pausa. Aqui, a execução do aplicativo acontece após o "yield"
    # Não há ações de término nesse caso, mas o "yield" permite a execução após a inicialização

# Inicializando a aplicação FastAPI com o contexto do lifespan definido acima
app = FastAPI(lifespan=lifespan)

# Incluindo as rotas de usuário e tarefas no aplicativo, com prefixos e tags para organização
app.include_router(user_routes, prefix="/user", tags=["Usuários"])  # Todas as rotas de usuários começam com "/user"
app.include_router(task_routes, prefix="/task", tags=["Tarefas"])  # Todas as rotas de tarefas começam com "/task"

# Definindo uma rota raiz simples que retorna uma mensagem de boas-vindas
@app.get("/")
async def root():
    return {"Mensagem:": "Olá mundo, este é uma API de Tarefas!"}
