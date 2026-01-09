# app/schemas/administracao.py
from pydantic import BaseModel, EmailStr

class AdminCreate(BaseModel):
    nome: str
    cargo: str
    email: EmailStr
    senha: str