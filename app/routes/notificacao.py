from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Notificacao, Medico
from app.schemas.notificacao import NotificacaoPacienteCreate, NotificacaoMedicoCreate, NotificacaoCreate
from app.auth import get_current_user  # função que pega o usuário do token
from app.models import Notificacao, Paciente
from app.security.dependencies import tem_permissao
from datetime import datetime



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

    # Filtra apenas mensagens enviadas por pacientes e admins
    notificacoes = db.query(Notificacao).filter(
        Notificacao.id_medico == medico.id_medico,
        Notificacao.remetente.in_(["paciente", "administracao"])
    ).all()

    resultado = []
    for n in notificacoes:
        if n.remetente == "paciente":
            paciente = db.query(Paciente).filter(Paciente.id_paciente == n.id_paciente).first()
            remetente_nome = paciente.nome if paciente else "Desconhecido"
        else:
            remetente_nome = "Administração"

        resultado.append({
            "remetente": remetente_nome,
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
        Notificacao.remetente.in_(["medico", "administracao"])
    ).all()

    resultado = []
    for n in notificacoes:
        if n.remetente == "medico":
            medico = db.query(Medico).filter(Medico.id_medico == n.id_medico).first()
            remetente_nome = medico.nome if medico else "Desconhecido"
        else:
            remetente_nome = "Administração"

        resultado.append({
            "remetente": remetente_nome,
            "mensagem": n.conteudo
        })

    return resultado




@router.post("/adm")
def enviar_notificacao(
    dados: NotificacaoCreate,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("enviar_notificacaoadm"))  # apenas admins
):
    # Resolve destinatário
    if dados.tipo == "paciente":
        destinatario = db.query(Paciente).filter(Paciente.id_paciente == dados.id_usuario).first()
        if not destinatario:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        id_paciente = dados.id_usuario
        id_medico = None
        nome_destinatario = destinatario.nome
    else:  # medico
        destinatario = db.query(Medico).filter(Medico.id_medico == dados.id_usuario).first()
        if not destinatario:
            raise HTTPException(status_code=404, detail="Médico não encontrado")
        id_paciente = None
        id_medico = dados.id_usuario
        nome_destinatario = destinatario.nome

    # Cria notificação com remetente automático
    nova = Notificacao(
        id_paciente=id_paciente,
        id_medico=id_medico,
        remetente="administracao",
        conteudo=dados.conteudo,
        data_hora=datetime.utcnow()
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)

    return {
        "msg": "Notificação enviada com sucesso",
        "destinatario": nome_destinatario,
        "tipo": dados.tipo,
        "conteudo": nova.conteudo,
        "data_hora": nova.data_hora
    }