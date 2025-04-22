from fastapi import FastAPI
from database.database import create_db_and_tables
from contextlib import asynccontextmanager
from routes.tasks_routes import router as task_routes
from routes.user_routes import router as user_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_routes, prefix="/user", tags=["Usuários"])
app.include_router(task_routes, prefix="/task", tags=["Tarefas"])
@app.get("/")
async def root():
    return  {"Mensagem:": "Olá mundo, este é uma API de Tarefas!"}
