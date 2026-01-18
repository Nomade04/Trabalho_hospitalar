from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.receita import Receita
from app.models.consulta import Consulta
from app.models.medico import Medico
from app.security.dependencies import tem_permissao
from app.schemas.receita import ReceitaCreate

router = APIRouter(prefix="/receita", tags=["receita"])

@router.post("")
def emitir_receita(
    dados: ReceitaCreate,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("emitir_receita"))
):
    # 1. Identifica o médico logado
    medico = None
    if user["email"].isdigit():
        medico = db.query(Medico).filter(Medico.id_medico == int(user["email"])).first()
    else:
        medico = db.query(Medico).filter(Medico.email == user["email"]).first()

    if not medico:
        raise HTTPException(status_code=403, detail="Somente médicos podem emitir receitas")

    # 2. Verifica se a consulta existe
    consulta = db.query(Consulta).filter(Consulta.id_consulta == dados.id_consulta).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    # 3. Cria a receita vinculada à consulta
    nova_receita = Receita(
        medicamentos=dados.medicamentos,
        data_emissao=date.today(),
        id_consulta=dados.id_consulta
    )

    db.add(nova_receita)
    db.commit()
    db.refresh(nova_receita)

    # 4. Retorno com o médico logado (quem emitiu)
    return {
        "msg": "Receita emitida com sucesso",
        "id": nova_receita.id,
        "medicamentos": nova_receita.medicamentos,
        "data_emissao": nova_receita.data_emissao,
        "id_consulta": nova_receita.id_consulta,
        "medico_emissor": medico.nome   # <- usa o médico logado
    }