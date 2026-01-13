from pydantic import BaseModel
from datetime import datetime

class ConsultaCreate(BaseModel):
    data_hora: datetime
    nome_medico: str
    tipo_presencial: bool
