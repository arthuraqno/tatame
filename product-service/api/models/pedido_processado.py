from sqlalchemy import Column, Integer
from base import Base

class PedidoProcessado(Base):

    __tablename__ = "pedidos_processados"

    id = Column(Integer, primary_key=True)
    pedido_id =	Column(Integer, nullable=False, unique=True)