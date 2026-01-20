from pydantic import BaseModel

class EstoqueCreate(BaseModel):
    nome_item: str
    quantidade: int
    categoria: str

class EstoqueFiltro(BaseModel):
    categoria: str  # Ex: "EPI", "Medicamentos", ou "tudo"

class EstoqueBaixa(BaseModel):
    id: int           # ID do item no estoque
    quantidade: int   # Quantidade a ser reduzida