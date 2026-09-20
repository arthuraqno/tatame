from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


ALGORITHM = "RS256"
TEMPO_EXPIRACAO_MINUTOS = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_scheme = HTTPBearer()

with open("private_key.pem", "r") as f:
    PRIVATE_KEY = f.read()

with open("public_key.pem", "r") as f:
    PUBLIC_KEY = f.read()

def criar_token(dados: dict):
    dados_copia = dados.copy()
    expira_em = datetime.utcnow() + timedelta(minutes=TEMPO_EXPIRACAO_MINUTOS)
    dados_copia.update({"exp": expira_em})
    token = jwt.encode(dados_copia, PRIVATE_KEY, algorithm=ALGORITHM)
    return token

def validar_token(token: str):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def gerar_hash_senha(senha:str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha_digitada:str,senha_hash:str) -> bool:
    return pwd_context.verify(senha_digitada, senha_hash)

def obter_usuario_atual(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    payload = validar_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    return payload