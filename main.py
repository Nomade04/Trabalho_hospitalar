from fastapi import FastAPI
from app.database import init_db
from app.routes import login, home,cadastro

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

# Inclui as rotas
app.include_router(home.router)
app.include_router(login.router)
app.include_router(cadastro.router)