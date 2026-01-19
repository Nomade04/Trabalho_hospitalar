from pydantic import BaseModel

class UsuarioDelete(BaseModel):
    id: int
    tipo: str  # "medico", "paciente" ou "administracao"