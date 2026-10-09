import enum
from base import Base
from sqlalchemy import Column, Integer, Numeric, String, DateTime, Enum
from datetime import datetime

class StatusPagamento(str, enum.Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    FALHOU = "falhou"

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, nullable=False)
    usuario_id = Column(Integer, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(StatusPagamento), nullable=False, default=StatusPagamento.PENDENTE)
    stripe_session_id = Column(String(255), nullable=False, unique=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
