from pydantic import BaseModel, field_validator
from datetime import datetime


class NotificacaoPacienteCreate(BaseModel):
    id_medico: int
    conteudo: str

    class Config:
        from_attributes = True  # Pydantic v2


class NotificacaoMedicoCreate(BaseModel):
    id_paciente: int
    conteudo: str

    class Config:
        from_attributes = True


class NotificacaoCreate(BaseModel):
    id_usuario: int        # id do médico ou paciente
    tipo: str              # "medico" ou "paciente"
    conteudo: str

    @field_validator("tipo")
    def validar_tipo(cls, v):
        v = v.lower()
        if v not in {"medico", "paciente"}:
            raise ValueError("tipo deve ser 'medico' ou 'paciente'")
        return v

from pydantic import BaseModel

class NotificacaoMedicoadmCreate(BaseModel):
    conteudo: str
