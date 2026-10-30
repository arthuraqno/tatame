from sqlalchemy import Column, Integer, String, BigInteger
from base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable= True)
    telefone = Column(String(100), nullable=True)
    role = Column(String(50), nullable=False, default="cliente")
    github_id = Column(BigInteger, unique=True, nullable=True)