from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.medico import Medico
from app.models.paciente import Paciente
from app.models.administracao import Administracao
from app.security.dependencies import tem_permissao
from app.schemas.usuario import UsuarioDelete

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/listar")
def listar_usuarios(
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("listar_usuarios"))
):
    medicos = db.query(Medico).all()
    pacientes = db.query(Paciente).all()
    admins = db.query(Administracao).all()

    resultado = {
        "medicos": [
            {"id": m.id_medico, "nome": m.nome, "email": m.email, "especialidade": m.especialidade}
            for m in medicos
        ],
        "pacientes": [
            {"id": p.id_paciente, "nome": p.nome, "email": p.email, "cpf": p.cpf}
            for p in pacientes
        ],
        "admins": [
            {"id": a.id_admin, "nome": a.nome, "email": a.email, "cargo": a.cargo}
            for a in admins
        ]
    }

    return resultado


@router.delete("/deletar")
def deletar_usuario(
    dados: UsuarioDelete,
    db: Session = Depends(get_db),
    user=Depends(tem_permissao("deletar_usuario"))
):
    if dados.tipo == "medico":
        usuario = db.query(Medico).filter(Medico.id_medico == dados.id).first()
    elif dados.tipo == "paciente":
        usuario = db.query(Paciente).filter(Paciente.id_paciente == dados.id).first()
    elif dados.tipo == "administracao":
        usuario = db.query(Administracao).filter(Administracao.id_admin == dados.id).first()
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuário inválido")

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    nome_usuario = usuario.nome  # pega o nome antes de deletar
    db.delete(usuario)
    db.commit()

    return {
        "msg": f"Usuário {dados.tipo} com id {dados.id} deletado com sucesso",
        "nome": nome_usuario
    }