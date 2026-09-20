from sqlalchemy import Column, Integer, Numeric, Boolean, String
from base import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(256), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(100), nullable=False)
    tamanho = Column(String(100), nullable=False)
    estoque = Column(Integer, nullable=False)
    imagem_url = Column(String(256), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)