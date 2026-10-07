from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

ALGORITHM = "RS256"

security_scheme = HTTPBearer()

with open("public_key.pem", "r") as f:
    PUBLIC_KEY = f.read()

def validar_token(token: str):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def obter_usuario_atual(credentials : HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    payload = validar_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token inválido ou expirado")
    return payload