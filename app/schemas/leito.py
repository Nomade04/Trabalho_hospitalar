from pydantic import BaseModel

class LeitoCreate(BaseModel):
    status_vago: bool
    localizacao: str

class LeitoUpdateStatus(BaseModel):
    status_vago: bool