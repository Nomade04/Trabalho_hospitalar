from fastapi import FastAPI
from app.database import init_db
from app.routes import login, home, cadastro, consulta, notificacao

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

# Inclui as rotas
app.include_router(home)
app.include_router(login)
app.include_router(cadastro)
app.include_router(consulta)
app.include_router(notificacao)   # agora notificacao já é o router

