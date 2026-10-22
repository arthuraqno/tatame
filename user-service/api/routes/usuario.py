from fastapi import APIRouter, HTTPException, status
from schemas.usuario import UsuarioResponse, UsuarioCreate, LoginRequest, TokenResponse
from services.usuario_service import UsuarioService

router = APIRouter()
usuario_service = UsuarioService()

@router.post("/usuarios", response_model=UsuarioResponse)
def cadastrar_usuario(dados: UsuarioCreate):
    return usuario_service.cadastrar_usuario(dados.email, dados.senha, dados.telefone)

@router.post("/usuarios/login", response_model=TokenResponse)
def login_usuario(dados: LoginRequest):
    resultado = usuario_service.login(dados.email, dados.senha)
    if resultado == "bloqueado":
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas de login. Tente novamente em alguns minutos."
        )
    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos")
    return TokenResponse(access_token=resultado, token_type="bearer")
