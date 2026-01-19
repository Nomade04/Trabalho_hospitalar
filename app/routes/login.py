from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.medico import Medico
from app.models.paciente import Paciente
from app.models.administracao import Administracao
from app.security.security import verificar_senha, criar_token_acesso
from app.schemas.login import LoginRequest

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    # Busca separada para cada tipo de usuário
    medico = db.query(Medico).filter(Medico.email == dados.email).first()
    paciente = db.query(Paciente).filter(Paciente.email == dados.email).first()
    admin = db.query(Administracao).filter(Administracao.email == dados.email).first()

    usuario = medico or paciente or admin

    if not usuario or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    # Identifica o tipo de usuário
    if medico:
        tipo = "medico"
        user_id = medico.id_medico
    elif paciente:
        tipo = "paciente"
        user_id = paciente.id_paciente
    elif admin:
        tipo = "administracao"
        user_id = admin.id_admin
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuário desconhecido")

    # Cria token JWT
    token = criar_token_acesso({"sub": str(user_id), "tipo": tipo})

    return {
        "access_token": token,
        "token_type": "bearer",
        "perfil": tipo,
        "nome": usuario.nome
    }
