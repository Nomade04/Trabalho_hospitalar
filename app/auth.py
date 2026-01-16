from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.medico import Medico
from app.models.paciente import Paciente
from app.models.administracao import Administracao
from app.security.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        tipo: str = payload.get("tipo")
        if user_id is None or tipo is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    if tipo == "medico":
        usuario = db.query(Medico).filter(Medico.id_medico == int(user_id)).first()
    elif tipo == "paciente":
        usuario = db.query(Paciente).filter(Paciente.id_paciente == int(user_id)).first()
    elif tipo == "administracao":
        usuario = db.query(Administracao).filter(Administracao.id_admin == int(user_id)).first()
    else:
        raise HTTPException(status_code=401, detail="Tipo de usuário inválido")

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario