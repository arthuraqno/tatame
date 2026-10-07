from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from models.pedido import StatusPedido

class ItemPedidoResponse(BaseModel):
    produto_id : int
    nome_produto : str
    quantidade : int 
    preco_unitario : Decimal
    subtotal : Decimal

class PedidoResponse(BaseModel):
    id : int
    status : StatusPedido
    total : Decimal
    criado_em : datetime
    itens: list[ItemPedidoResponse]