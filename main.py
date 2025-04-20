from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return  {"Mensagem:": "Olá mundo, este é uma API de Tarefas!"}
