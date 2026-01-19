from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.estoque import Estoque
from app.schemas.estoque import EstoqueCreate, EstoqueFiltro
from app.security.dependencies import tem_permissao

router = APIRouter(prefix="/estoque", tags=["estoque"])

@router.post("/adicionar")
def adicionar_item(
    dados: EstoqueCreate,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("adicionar_estoque"))
):
    novo_item = Estoque(
        nome_item=dados.nome_item,
        quantidade=dados.quantidade,
        categoria=dados.categoria
    )
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)

    return {
        "msg": "Item adicionado ao estoque com sucesso",
        "id": novo_item.id,
        "nome_item": novo_item.nome_item,
        "quantidade": novo_item.quantidade,
        "categoria": novo_item.categoria
    }



@router.post("/listar")
def listar_estoque(
    filtro: EstoqueFiltro,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("listar_estoque"))
):
    if filtro.categoria.lower() == "tudo":
        itens = db.query(Estoque).all()
    else:
        itens = db.query(Estoque).filter(Estoque.categoria == filtro.categoria).all()

    return [
        {
            "id": item.id,
            "nome_item": item.nome_item,
            "quantidade": item.quantidade,
            "categoria": item.categoria
        }
        for item in itens
    ]