from pydantic import BaseModel

class EstoqueCreate(BaseModel):
    nome_item: str
    quantidade: int
    categoria: str

from pydantic import BaseModel

class EstoqueFiltro(BaseModel):
    categoria: str  # Ex: "EPI", "Medicamentos", ou "tudo"