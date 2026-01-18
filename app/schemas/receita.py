from pydantic import BaseModel

class ReceitaCreate(BaseModel):
    medicamentos: str
    id_consulta: int