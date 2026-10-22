from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioResponse
from database import engine
from auth import gerar_hash_senha, verificar_senha, criar_token
from redis_client import redis_client
from mensageria import publicar_evento

LIMITE_FALHAS = 5
JANELA_SEGUNDOS = 15 * 60
class UsuarioService:
    def cadastrar_usuario(self, email, senha, telefone, ):
        with Session(engine) as session:
            senha_hash = gerar_hash_senha(senha)
            usuario = Usuario(
                email=email,
                senha_hash=senha_hash,
                telefone=telefone)
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            try:
                publicar_evento("usuario.criado", {
                    "usuario_id": usuario.id,
                    "email": usuario.email,
                    "telefone": usuario.telefone,
                })
            except Exception as erro:
                print(f"Falha ao publicar usuario.criado: {erro}")
            return self._to_response(usuario)

    def _to_response(self, usuario: Usuario) -> UsuarioResponse:
        return UsuarioResponse(
            id=usuario.id,
            email=usuario.email,
            role=usuario.role,
            telefone=usuario.telefone)
    
    def login(self, email:str, senha:str):
        if self.login_bloqueado(email):
            return "bloqueado"
        
        with Session(engine) as session:
            usuario = session.query(Usuario).filter(Usuario.email == email).first()

            if usuario is None or not verificar_senha(senha, usuario.senha_hash):
                self.registrar_falha(email)
                return None
            
            self.limpar_falhas(email)
            token = criar_token({"sub": str(usuario.id), "role": usuario.role})
            return token

    def _chave_falhas(self, email: str) -> str:
        return f"login:falhas:{email.lower()}"

    def login_bloqueado(self, email: str) -> bool:
        falhas = redis_client.get(self._chave_falhas(email))
        return falhas is not None and int(falhas) >= LIMITE_FALHAS

    def registrar_falha(self, email: str):
        chave = self._chave_falhas(email)
        redis_client.incr(chave)
        redis_client.expire(chave, JANELA_SEGUNDOS)

    def limpar_falhas(self, email: str):
        redis_client.delete(self._chave_falhas(email))
