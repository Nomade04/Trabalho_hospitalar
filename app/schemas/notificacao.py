from pydantic import BaseModel
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
