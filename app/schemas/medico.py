# app/schemas/medico.py
from pydantic import BaseModel, EmailStr

class MedicoCreate(BaseModel):
    nome: str
    cmr: str
    especialidade: str
    telefone: str
    email: EmailStr
    senha: str