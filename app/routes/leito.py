from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.leito import Leito
from app.security.dependencies import tem_permissao
from app.schemas.leito import LeitoCreate, LeitoUpdateStatus

router = APIRouter(prefix="/leito", tags=["leito"])

@router.post("/cadastrar")
def cadastrar_leito(
    dados: LeitoCreate,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("cadastrar_leito"))
):
    novo_leito = Leito(
        status_vago=dados.status_vago,
        localizacao=dados.localizacao
    )
    db.add(novo_leito)
    db.commit()
    db.refresh(novo_leito)
    return {"msg": "Leito cadastrado com sucesso", "id": novo_leito.id}

@router.get("/listar")
def listar_leitos(
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("listar_leitos"))
):
    leitos = db.query(Leito).all()
    return [
        {
            "id": leito.id,
            "status_vago": leito.status_vago,
            "localizacao": leito.localizacao
        }
        for leito in leitos
    ]

@router.patch("/{leito_id}")
def atualizar_status_leito(
    leito_id: int,
    dados: LeitoUpdateStatus,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("atualizar_leito"))
):
    leito = db.query(Leito).filter(Leito.id == leito_id).first()
    if not leito:
        raise HTTPException(status_code=404, detail="Leito não encontrado")

    leito.status_vago = dados.status_vago
    db.commit()
    db.refresh(leito)

    return {
        "msg": "Status do leito atualizado com sucesso",
        "id": leito.id,
        "status_vago": leito.status_vago,
        "localizacao": leito.localizacao
    }