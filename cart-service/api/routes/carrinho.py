from fastapi import APIRouter, HTTPException, status, Depends
from schemas.carrinho import CarrinhoResponse, ItemRequest, AtualizarQuantidadeRequest
from services.carrinho_service import CarrinhoService
from auth import obter_usuario_atual

router = APIRouter()
carrinho_service = CarrinhoService()

@router.post("/carrinho/itens", response_model= CarrinhoResponse)
def adcionar_item(dados: ItemRequest, usuario_atual: dict = Depends(obter_usuario_atual)):
   usuario_id = int(usuario_atual.get("sub"))
   resultado = carrinho_service.adcionar_item(usuario_id, dados.produto_id, dados.quantidade)
   if resultado is None:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="Produto não encontrado ou estoque insuficiente"
      )
   return carrinho_service.ver_carrinho(usuario_id)

@router.get("/carrinho", response_model=CarrinhoResponse)
def ver_carrinho(usuario_atual: dict = Depends(obter_usuario_atual)):
   usuario_id = int(usuario_atual.get("sub"))
   return carrinho_service.ver_carrinho(usuario_id)

@router.delete("/carrinho/itens/{produto_id}")
def remover_item(produto_id:int, usuario_atual: dict = Depends(obter_usuario_atual)):
   usuario_id = int(usuario_atual.get("sub"))
   resultado = carrinho_service.remover_item(usuario_id, produto_id)
   if resultado is False:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail= "Produto não estava no carrinho"
      )
   return {"mensagem": "Produto removido do carrinho"}
   
@router.put("/carrinho/itens/{produto_id}", response_model=CarrinhoResponse)
def atualizar_item(produto_id: int, dados: AtualizarQuantidadeRequest, usuario_atual: dict = Depends(obter_usuario_atual)):
   usuario_id = int(usuario_atual.get("sub"))
   resultado = carrinho_service.atualizar_quantidade(usuario_id, produto_id, dados.quantidade)
   if resultado is None:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="Produto não encontrado ou estoque insuficiente"
      )
   return carrinho_service.ver_carrinho(usuario_id)

@router.delete("/carrinho")
def limpar_carrinho(usuario_atual: dict = Depends(obter_usuario_atual)):
   usuario_id = int(usuario_atual.get("sub"))
   resultado = carrinho_service.limpar_carrinho(usuario_id) 
   return {"mensagem": "Carrinho esvaziado"}
