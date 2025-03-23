from fastapi import FastAPI
from app.routes import tasks
from app.database import engine, Base

# Criar tabelas no banco de dados automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir as rotas da API
app.include_router(tasks.router)

@app.get("/")
def home():
    return {"message": "Bem-vindo à API de To-Do List!"}
 
