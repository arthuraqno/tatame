import os
import secrets
from urllib.parse import urlencode
from redis_client import redis_client
import httpx

GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API = "https://api.github.com"
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_REDIRECT_URI = "http://127.0.0.1:8001/auth/github/callback"
STATE_VALIDADE_SEGUNDOS = 10 * 60


class OAuthService:
    def gerar_url_github(self) -> str:
        state = secrets.token_urlsafe(32)
        redis_client.set(f"oauth:state:{state}", "1", ex=STATE_VALIDADE_SEGUNDOS)
        parametros = urlencode({
            "client_id": GITHUB_CLIENT_ID,
            "redirect_uri": GITHUB_REDIRECT_URI,
            "scope": "user:email",
            "state": state,
        })
        return f"{GITHUB_AUTHORIZE_URL}?{parametros}"
    
    def validar_state(self, state: str | None) -> bool:
        if not state:
            return False
        return redis_client.delete(f"oauth:state:{state}") == 1

    def trocar_code_por_token(self, code: str):
        resposta = httpx.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
            timeout=10,
        )
        if resposta.status_code != 200:
            return None
        return resposta.json().get("access_token")

    def buscar_identidade(self, access_token: str):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        }
        perfil = httpx.get(f"{GITHUB_API}/user", headers=headers, timeout=10)
        if perfil.status_code != 200:
            return None

        email = None
        emails = httpx.get(f"{GITHUB_API}/user/emails", headers=headers, timeout=10)
        if emails.status_code == 200:
            for item in emails.json():
                if item.get("primary") and item.get("verified"):
                    email = item["email"]
                    break

        dados = perfil.json()
        return {"github_id": dados["id"], "login": dados["login"], "email": email}