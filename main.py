from fastapi import FastAPI
from app.database import init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()   # cria banco e tabelas se não existirem


@app.get("/")
def home():
    return {"mensagem": "API Hospital rodando com sucesso!"}

