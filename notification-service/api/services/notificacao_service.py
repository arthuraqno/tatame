from sqlalchemy.orm import Session
from database import engine
from models.contato import Contato

class NotificationService:
    def guardar_contato(self, usuario_id, email, telefone):
        with Session(engine) as session:
            contato = session.query(Contato).filter(Contato.usuario_id == usuario_id).first()
            if contato is not None:
                return False
            contato = Contato(
                usuario_id=usuario_id,
                email=email,
                telefone=telefone)
            session.add(contato)
            session.commit()
            return True

    def montar_mensagem(self, dados):
        with Session(engine) as session:
            contato = session.query(Contato).filter(Contato.usuario_id == dados["usuario_id"]).first()
            if contato is None:
                print(f"Contato do usuário {dados['usuario_id']} não encontrado")
                return None
            return{
                "para" : contato.email,
                "assunto" : f"Pedido #{dados['pedido_id']} confirmado",
                "texto" : f"Olá! Recebemos o pagamento do seu pedido #{dados['pedido_id']}. Obrigado por comprar no Tatame!"}