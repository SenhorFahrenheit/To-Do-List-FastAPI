from fastapi import FastAPI
from database.database import create_db_and_tables
from contextlib import asynccontextmanager
from routes.tasks_routes import router as router_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_routes)
@app.get("/")
async def root():
    return  {"Mensagem:": "Olá mundo, este é uma API de Tarefas!"}
