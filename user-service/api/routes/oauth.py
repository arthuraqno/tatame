from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from services.oauth_service import OAuthService
from services.usuario_service import UsuarioService
from schemas.usuario import TokenResponse

router = APIRouter()
oauth_service = OAuthService()
usuario_service = UsuarioService()


@router.get("/auth/github/login")
def login_github():
    return RedirectResponse(oauth_service.gerar_url_github())


@router.get("/auth/github/callback", response_model=TokenResponse)
def callback_github(code: str | None = None, state: str | None = None):
    if code is None or not oauth_service.validar_state(state):
        raise HTTPException(status_code=400, detail="Requisição inválida")

    access_token = oauth_service.trocar_code_por_token(code)
    if access_token is None:
        raise HTTPException(status_code=400, detail="Falha ao autenticar com o GitHub")

    identidade = oauth_service.buscar_identidade(access_token)
    if identidade is None:
        raise HTTPException(status_code=400, detail="Falha ao ler a identidade no GitHub")

    resultado, token = usuario_service.login_github(identidade)

    if resultado == "sem_email":
        raise HTTPException(status_code=400, detail="O GitHub não devolveu um e-mail verificado")
    if resultado == "conflito":
        raise HTTPException(status_code=409, detail="Já existe uma conta com este e-mail. Entre com e-mail e senha.")
    return TokenResponse(access_token=token, token_type="bearer")