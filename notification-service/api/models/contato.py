from sqlalchemy import Column, Integer, String
from base import Base

class Contato(Base):
    __tablename__ = "contatos"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False, unique=True)
    email = Column(String(256), nullable=False)
    telefone = Column(String(30), nullable=True)