from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.relatorio import Relatorio
from app.models.medico import Medico
from app.models.administracao import Administracao
from app.security.dependencies import tem_permissao
from app.schemas.relatorio import RelatorioCreate

router = APIRouter(prefix="/relatorio", tags=["relatorio"])

@router.post("/")
def criar_relatorio(
    dados: RelatorioCreate,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("criar_relatorio"))
):
    # Se for médico logado
    if user["tipo"] == "medico":
        medico = db.query(Medico).filter(Medico.email == user["email"]).first()
        if not medico:
            raise HTTPException(status_code=403, detail="Médico não encontrado")
        relatorio = Relatorio(
            tipo=dados.tipo,
            data_geracao=date.today(),
            id_medico=medico.id_medico,
            id_admin=None
        )
        emitido_por = medico.nome

    # Se for administrador logado
    elif user["tipo"] == "admin":
        admin = db.query(Administracao).filter(Administracao.email == user["email"]).first()
        if not admin:
            raise HTTPException(status_code=403, detail="Administrador não encontrado")
        relatorio = Relatorio(
            tipo=dados.tipo,
            data_geracao=date.today(),
            id_medico=None,
            id_admin=admin.id_admin
        )
        emitido_por = admin.nome

    else:
        raise HTTPException(status_code=403, detail="Somente médicos ou administradores podem criar relatórios")

    db.add(relatorio)
    db.commit()
    db.refresh(relatorio)

    return {
        "msg": "Relatório criado com sucesso",
        "id": relatorio.id,
        "tipo": relatorio.tipo,
        "data_geracao": relatorio.data_geracao,
        "emitido_por": emitido_por
    }