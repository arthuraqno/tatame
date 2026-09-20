from pydantic import BaseModel
from decimal import Decimal

class ProdutoCreate(BaseModel):
    nome : str
    descricao : str
    preco : Decimal
    categoria: str
    tamanho : str
    estoque : int
    imagem_url : str

class ProdutoResponse(BaseModel):
    id : int
    nome : str
    descricao : str
    preco : Decimal
    categoria: str
    tamanho : str
    estoque : int
    imagem_url : str
    ativo : bool

class ProdutoUpdate(BaseModel):
    nome : str | None = None 
    preco : Decimal | None = None
    categoria: str | None = None
    tamanho : str | None = None
    estoque : int | None = None
    imagem_url : str | None = None