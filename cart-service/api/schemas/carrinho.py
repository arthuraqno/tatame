from pydantic import BaseModel, Field
from decimal import Decimal

class ItemRequest(BaseModel):
    produto_id : int
    quantidade : int

class ItemCarrinho(BaseModel):
    produto_id : int
    nome : str
    preco : Decimal
    quantidade : int
    subtotal : Decimal

class CarrinhoResponse(BaseModel):
    itens : list[ItemCarrinho]
    total : Decimal

class AtualizarQuantidadeRequest(BaseModel):
    quantidade: int = Field(gt=0)