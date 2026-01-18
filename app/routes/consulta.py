from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consulta import Consulta
from app.models.medico import Medico
from app.models.paciente import Paciente
from app.schemas.consulta import ConsultaCreate
from app.security.dependencies import tem_permissao, get_current_user

router = APIRouter(prefix="/consulta", tags=["consulta"])

@router.post("/agendar")
def agendar_consulta(
    dados: ConsultaCreate,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("agendar_consulta"))
):
    # Tenta interpretar o "email" do token como id ou email
    paciente = None
    if user["email"].isdigit():
        # se for número, busca pelo id
        paciente = db.query(Paciente).filter(Paciente.id_paciente == int(user["email"])).first()
    else:
        # se for texto, busca pelo email
        paciente = db.query(Paciente).filter(Paciente.email == user["email"]).first()

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Buscar médico pelo nome informado
    medico = db.query(Medico).filter(Medico.nome == dados.nome_medico).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    nova_consulta = Consulta(
        data_hora=dados.data_hora,
        status="agendada",
        tipo_presencial=dados.tipo_presencial,
        id_paciente=paciente.id_paciente,
        id_medico=medico.id_medico
    )
    db.add(nova_consulta)
    db.commit()
    db.refresh(nova_consulta)
    return {"msg": "Consulta agendada com sucesso", "id": nova_consulta.id_consulta}

@router.delete("/cancelar/{id_consulta}")
def cancelar_consulta(
    id_consulta: int,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("cancelar_consulta"))
):
    consulta = db.query(Consulta).filter(Consulta.id_consulta == id_consulta).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    # Verifica se o paciente logado é o dono da consulta
    paciente = None
    if user["email"].isdigit():
        # se o "sub" do token for id
        paciente = db.query(Paciente).filter(Paciente.id_paciente == int(user["email"])).first()
    else:
        # se for email
        paciente = db.query(Paciente).filter(Paciente.email == user["email"]).first()

    if not paciente or consulta.id_paciente != paciente.id_paciente:
        raise HTTPException(status_code=403, detail="Você só pode cancelar suas próprias consultas")

    consulta.status = "cancelada"
    db.commit()
    return {"msg": "Consulta cancelada com sucesso"}

@router.post("/chamar")
def chamar_consulta(
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("chamar_consulta"))
):
    # Identifica o médico logado pelo token (id ou email)
    medico = None
    if user["email"].isdigit():
        medico = db.query(Medico).filter(Medico.id_medico == int(user["email"])).first()
    else:
        medico = db.query(Medico).filter(Medico.email == user["email"]).first()

    if not medico:
        raise HTTPException(status_code=403, detail="Somente médicos podem chamar consultas")

    # Busca a próxima consulta agendada para esse médico (mais próxima pela data/hora)
    consulta = (
        db.query(Consulta)
        .filter(Consulta.id_medico == medico.id_medico, Consulta.status == "agendada")
        .order_by(Consulta.data_hora.asc())
        .first()
    )

    if not consulta:
        raise HTTPException(status_code=404, detail="Nenhuma consulta agendada encontrada")

    # Atualiza status para finalizada
    consulta.status = "finalizada"
    db.commit()
    db.refresh(consulta)

    # Busca dados do paciente
    paciente = db.query(Paciente).filter(Paciente.id_paciente == consulta.id_paciente).first()

    return {
        "msg": "Consulta chamada e finalizada com sucesso",
        "id_consulta": consulta.id_consulta,
        "data_hora": consulta.data_hora,
        "paciente": {
            "id": paciente.id_paciente,
            "nome": paciente.nome,
            "email": paciente.email
        }
    }