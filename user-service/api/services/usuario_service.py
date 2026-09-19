from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioResponse
from database import engine
from auth import gerar_hash_senha, verificar_senha, criar_token

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
            return self._to_response(usuario)

    def _to_response(self, usuario: Usuario) -> UsuarioResponse:
        return UsuarioResponse(
            id=usuario.id,
            email=usuario.email,
            role=usuario.role,
            telefone=usuario.telefone)
    
    def login(self, email:str, senha:str):
        with Session(engine) as session:
            usuario = session.query(Usuario).filter(Usuario.email == email).first()

            if usuario is None:
                return None
            if not verificar_senha(senha, usuario.senha_hash):
                return None

            token = criar_token({"sub": str(usuario.id), "role": usuario.role})
            return token


