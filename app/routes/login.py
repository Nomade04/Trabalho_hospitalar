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
    usuario = (
        db.query(Medico).filter(Medico.email == dados.email).first()
        or db.query(Paciente).filter(Paciente.email == dados.email).first()
        or db.query(Administracao).filter(Administracao.email == dados.email).first()
    )

    if not usuario or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    tipo = usuario.__tablename__
    if tipo == "medico":
        user_id = usuario.id_medico
    elif tipo == "paciente":
        user_id = usuario.id_paciente
    elif tipo == "administracao":
        user_id = usuario.id_admin
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuário desconhecido")

    token = criar_token_acesso({"sub": str(user_id), "tipo": tipo})

    return {
        "access_token": token,
        "token_type": "bearer",
        "perfil": tipo,
        "nome": usuario.nome
    }
