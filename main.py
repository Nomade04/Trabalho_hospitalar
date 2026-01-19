from fastapi import FastAPI
from app.database import init_db
from app.routes.__init__ import *
app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

# Inclui as rotas
app.include_router(home)
app.include_router(login)
app.include_router(cadastro)
app.include_router(consulta)
app.include_router(notificacao)
app.include_router(agenda)
app.include_router(prontuario)
app.include_router(receita)
app.include_router(relatorio)
app.include_router(leito)
app.include_router(usuarios)
app.include_router(estoque)





