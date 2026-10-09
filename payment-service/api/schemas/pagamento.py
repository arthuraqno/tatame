from pydantic import BaseModel
from decimal import Decimal
from models.pagamento import StatusPagamento

class PagamentoCreate(BaseModel):
    pedido_id : int

class PagamentoResponse(BaseModel):
    id : int
    pedido_id : int
    valor : Decimal
    status : StatusPagamento
    checkout_url : str