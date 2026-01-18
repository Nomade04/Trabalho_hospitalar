from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.prontuario import Prontuario
from app.models.medico import Medico
from app.security.dependencies import tem_permissao
from app.schemas.prontuario import ProntuarioUpdate

router = APIRouter(prefix="/prontuario", tags=["prontuario"])

# 1. Buscar prontuário de um paciente
@router.get("/{id_paciente}")
def obter_prontuario(
    id_paciente: int,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("visualizar_prontuario"))
):
    # valida médico logado (permissão)
    medico = db.query(Medico).filter(
        Medico.id_medico == int(user["email"]) if user["email"].isdigit() else Medico.email == user["email"]
    ).first()
    if not medico:
        raise HTTPException(status_code=403, detail="Somente médicos podem acessar prontuários")

    prontuario = db.query(Prontuario).filter(Prontuario.id_paciente == id_paciente).first()
    if not prontuario:
        raise HTTPException(status_code=404, detail="Prontuário não encontrado")

    # Formata histórico em lista (cada linha vira um item)
    historico = []
    if prontuario.observacoes:
        for linha in prontuario.observacoes.split("\n"):
            if linha.strip():
                historico.append(linha.strip())

    return {
        "id": prontuario.id,
        "historico": historico,  # cada item já contém [data - nome do médico] texto
        "data_atualizacao": prontuario.data_atualizacao,
        "ultimo_medico_id": prontuario.id_medico,
        "id_paciente": prontuario.id_paciente
    }

@router.put("/{id_paciente}")
def atualizar_prontuario(
    id_paciente: int,
    dados: ProntuarioUpdate,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("editar_prontuario"))
):
    # Médico logado
    medico = db.query(Medico).filter(
        Medico.id_medico == int(user["email"]) if user["email"].isdigit() else Medico.email == user["email"]
    ).first()

    if not medico:
        raise HTTPException(status_code=403, detail="Somente médicos podem editar prontuários")

    # Prontuário único por paciente
    prontuario = db.query(Prontuario).filter(Prontuario.id_paciente == id_paciente).first()

    linha = f"[{date.today()} - {medico.nome}] {dados.observacoes}"

    if prontuario:
        prontuario.observacoes = (prontuario.observacoes + "\n" + linha) if prontuario.observacoes else linha
        prontuario.data_atualizacao = date.today()
        prontuario.id_medico = medico.id_medico  # último médico que atualizou
        db.commit()
        db.refresh(prontuario)
        msg = "Prontuário atualizado com sucesso"
    else:
        prontuario = Prontuario(
            observacoes=linha,
            data_atualizacao=date.today(),
            id_medico=medico.id_medico,  # primeiro médico que criou
            id_paciente=id_paciente
        )
        db.add(prontuario)
        db.commit()
        db.refresh(prontuario)
        msg = "Prontuário criado com sucesso"

    return {
        "msg": msg,
        "id": prontuario.id,
        "observacoes": prontuario.observacoes,
        "data_atualizacao": prontuario.data_atualizacao,
        "ultimo_medico_id": prontuario.id_medico,
        "id_paciente": prontuario.id_paciente
    }