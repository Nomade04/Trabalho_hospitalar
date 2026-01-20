from pydantic import BaseModel
from datetime import datetime

class ConsultaCreate(BaseModel):
    data_hora: datetime
    nome_medico: str
    tipo_presencial: bool

class ConsultaUpdate(BaseModel):
    id_consulta: int
    data_hora: datetime
    status: str
    id_medico: int   # novo médico responsável (FK)

class ConsultaCancel(BaseModel):
    id_consulta: int


class ConsultaCreateADM(BaseModel):
    data_hora: datetime
    status: str
    tipo_presencial: bool
    id_paciente: int
    id_medico: int