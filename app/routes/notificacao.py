from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Notificacao, Medico
from app.schemas.notificacao import NotificacaoPacienteCreate, NotificacaoMedicoCreate
from app.auth import get_current_user  # função que pega o usuário do token
from app.models import Notificacao, Paciente

router = APIRouter(prefix="/notificacao", tags=["notificacao"])

@router.post("/enviar")
def enviar_notificacao(
    dados: NotificacaoPacienteCreate,
    db: Session = Depends(get_db),
    paciente=Depends(get_current_user)  # aqui vem o paciente logado
):
    # Confere se o médico existe
    medico = db.query(Medico).filter(Medico.id_medico == dados.id_medico).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    # Cria a notificação usando o id_paciente do token
    notificacao = Notificacao(
        conteudo=dados.conteudo,
        remetente="paciente",
        id_medico=dados.id_medico,
        id_paciente=paciente.id_paciente  # vem do token
    )
    db.add(notificacao)
    db.commit()
    db.refresh(notificacao)
    return notificacao


@router.get("/medico")
def listar_mensagens_medico(
    db: Session = Depends(get_db),
    medico=Depends(get_current_user)
):
    if not hasattr(medico, "id_medico"):
        raise HTTPException(status_code=403, detail="Somente médicos podem acessar suas notificações")

    # Filtra apenas mensagens enviadas por pacientes
    notificacoes = db.query(Notificacao).filter(
        Notificacao.id_medico == medico.id_medico,
        Notificacao.remetente == "paciente"
    ).all()

    resultado = []
    for n in notificacoes:
        paciente = db.query(Paciente).filter(Paciente.id_paciente == n.id_paciente).first()
        resultado.append({
            "remetente": paciente.nome if paciente else "Desconhecido",
            "mensagem": n.conteudo
        })

    return resultado

@router.post("/enviar-medico")
def enviar_notificacao_medico(
    dados: NotificacaoMedicoCreate,  # aqui você pode criar um schema específico se quiser
    db: Session = Depends(get_db),
    medico=Depends(get_current_user)  # médico logado
):
    # garante que o token seja de um médico
    if not hasattr(medico, "id_medico"):
        raise HTTPException(status_code=403, detail="Somente médicos podem enviar notificações")

    paciente = db.query(Paciente).filter(Paciente.id_paciente == dados.id_paciente).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    notificacao = Notificacao(
        conteudo=dados.conteudo,
        remetente="medico",
        id_medico=medico.id_medico,
        id_paciente=dados.id_paciente
    )
    db.add(notificacao)
    db.commit()
    db.refresh(notificacao)
    return notificacao

@router.get("/paciente")
def listar_mensagens_paciente(
    db: Session = Depends(get_db),
    paciente=Depends(get_current_user)
):
    if not hasattr(paciente, "id_paciente"):
        raise HTTPException(status_code=403, detail="Somente pacientes podem acessar suas notificações")

    # Filtra apenas mensagens enviadas por médicos
    notificacoes = db.query(Notificacao).filter(
        Notificacao.id_paciente == paciente.id_paciente,
        Notificacao.remetente == "medico"
    ).all()

    resultado = []
    for n in notificacoes:
        medico = db.query(Medico).filter(Medico.id_medico == n.id_medico).first()
        resultado.append({
            "remetente": medico.nome if medico else "Desconhecido",
            "mensagem": n.conteudo
        })

    return resultado