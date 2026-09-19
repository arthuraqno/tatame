from sqlalchemy import Column, Integer, String
from base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable= False)
    telefone = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default="cliente")
