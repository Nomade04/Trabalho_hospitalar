# app/schemas/paciente.py
from pydantic import BaseModel, EmailStr
from datetime import date

class PacienteCreate(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    email: EmailStr
    senha: str