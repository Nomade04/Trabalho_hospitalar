from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.models.consulta import Consulta
from app.security.dependencies import tem_permissao

router = APIRouter(prefix="/agenda", tags=["agenda"])

@router.get("")
def listar_agenda_medico(
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("listar_consultas_medico"))
):
    # Identifica o médico logado pelo token (id ou email)
    medico = None
    if user["email"].isdigit():
        medico = db.query(Medico).filter(Medico.id_medico == int(user["email"])).first()
    else:
        medico = db.query(Medico).filter(Medico.email == user["email"]).first()

    if not medico:
        raise HTTPException(status_code=403, detail="Somente médicos podem acessar suas consultas")

    # Filtra apenas consultas com status "agendada"
    consultas = db.query(Consulta).filter(
        Consulta.id_medico == medico.id_medico,
        Consulta.status == "agendada"
    ).all()

    resultado = []
    for c in consultas:
        paciente = db.query(Paciente).filter(Paciente.id_paciente == c.id_paciente).first()
        resultado.append({
            "id_consulta": c.id_consulta,
            "data_hora": c.data_hora,
            "status": c.status,
            "tipo_presencial": c.tipo_presencial,
            "paciente": paciente.nome if paciente else "Desconhecido"
        })

    return resultado