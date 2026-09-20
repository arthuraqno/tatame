from fastapi import APIRouter, HTTPException, status, Depends
from schemas.produto import ProdutoResponse, ProdutoCreate, ProdutoUpdate
from services.produto_service import ProdutoService
from auth import obter_usuario_atual

router = APIRouter()
produto_service = ProdutoService()

@router.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos():
    return produto_service.listar_produtos()

@router.get("/produtos/{id}", response_model=ProdutoResponse)
def buscar_produto(id : int):
    produto = produto_service.buscar_produto(id)
    if produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Produto não encontrado")
    return produto

@router.post("/produtos", response_model=ProdutoResponse)
def cadastrar_produto(dados: ProdutoCreate, usuario_atual: dict = Depends(obter_usuario_atual)):
    if usuario_atual.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem cadastrar produtos")
    return produto_service.cadastrar_produto(
        dados.nome, dados.descricao,
        dados.preco, dados.categoria,
        dados.tamanho, dados.estoque,
        dados.imagem_url)

@router.put("/produtos/{id}", response_model=ProdutoResponse)
def atualizar_produto(id: int, dados: ProdutoUpdate, usuario_atual: dict = Depends(obter_usuario_atual)):
    if usuario_atual.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores podem cadastrar produtos")
    produto = produto_service.atualizar_produto(
        id, dados.nome, dados.descricao,
        dados.preco, dados.categoria,
        dados.tamanho, dados.estoque,
        dados.imagem_url)
    if produto is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Produto não encontrado")
    return produto
    

@router.delete("/produtos/{id}")
def deletar_produto(id: int, usuario_atual: dict = Depends(obter_usuario_atual)):
     if usuario_atual.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem cadastrar produtos")
     produto = produto_service.deletar_produto(id)
     if produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Produto não encontrado")
     return produto