# app/security/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.security.security import SECRET_KEY, ALGORITHM
from app.security.permissoes  import PERMISSOES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print("TOKEN DECODIFICADO:", payload)

        email: str = payload.get("sub")
        tipo: str = payload.get("tipo")

        if email is None or tipo is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"email": email, "tipo": tipo}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def tem_permissao(acao: str):
    def checker(user=Depends(get_current_user)):
        tipo = user["tipo"]
        if acao not in PERMISSOES.get(tipo, set()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissão negada: perfil '{tipo}' não pode executar '{acao}'"
            )
        return user
    return checker