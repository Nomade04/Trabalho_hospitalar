# app/routes/cadastro.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.models.administracao import Administracao
from app.security.security import hash_senha
from app.schemas.paciente import PacienteCreate
from app.schemas.medico import MedicoCreate
from app.schemas.administracao import AdminCreate

router = APIRouter(prefix="/cadastro", tags=["cadastro"])

@router.post("/paciente")
def cadastrar_paciente(dados: PacienteCreate, db: Session = Depends(get_db)):
    if db.query(Paciente).filter(Paciente.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if db.query(Paciente).filter(Paciente.cpf == dados.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    usuario = Paciente(
        nome=dados.nome,
        cpf=dados.cpf,
        data_nascimento=dados.data_nascimento,
        telefone=dados.telefone,
        email=dados.email,
        senha=hash_senha(dados.senha)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return {"msg": "Paciente cadastrado com sucesso", "id": usuario.id_paciente}

@router.post("/medico")
def cadastrar_medico(dados: MedicoCreate, db: Session = Depends(get_db)):
    if db.query(Medico).filter(Medico.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if db.query(Medico).filter(Medico.cmr == dados.cmr).first():
        raise HTTPException(status_code=400, detail="CMR já cadastrado")

    usuario = Medico(
        nome=dados.nome,
        cmr=dados.cmr,
        especialidade=dados.especialidade,
        telefone=dados.telefone,
        email=dados.email,
        senha=hash_senha(dados.senha)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return {"msg": "Médico cadastrado com sucesso", "id": usuario.id_medico}

@router.post("/admin")
def cadastrar_admin(dados: AdminCreate, db: Session = Depends(get_db)):
    if db.query(Administracao).filter(Administracao.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    usuario = Administracao(
        nome=dados.nome,
        cargo=dados.cargo,
        email=dados.email,
        senha=hash_senha(dados.senha)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return {"msg": "Admin cadastrado com sucesso", "id": usuario.id_admin}