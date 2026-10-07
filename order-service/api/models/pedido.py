import enum
from base import Base
from sqlalchemy import Column, Integer, Numeric, DateTime, Enum
from datetime import datetime

class StatusPedido(str, enum.Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    ENVIADO = "enviado"
    CANCELADO = "cancelado"

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)
    status = Column(Enum(StatusPedido), nullable=False, default=StatusPedido.PENDENTE)
    total = Column(Numeric(10, 2), nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    