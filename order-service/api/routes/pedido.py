from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.pedido import ItemPedidoResponse, PedidoResponse, StatusPedido
from services.order_service import OrderService
from auth import obter_usuario_atual

router = APIRouter()
order_service = OrderService()
security_scheme = HTTPBearer()

@router.post("/pedidos", response_model= PedidoResponse)
def criar_pedido(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    usuario_atual: dict = Depends(obter_usuario_atual)):
    usuario_id = int(usuario_atual.get("sub")) 
    token = credentials.credentials
    pedido = order_service.criar_pedido(usuario_id, token)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Carrinho vazio ou indisponível"
        )
    return pedido

@router.get("/pedidos", response_model= list[PedidoResponse])
def listar_pedidos(usuario_atual: dict = Depends(obter_usuario_atual)):
    usuario_id = int(usuario_atual.get("sub"))
    return order_service.listar_pedidos(usuario_id)

@router.get("/pedidos/{pedido_id}", response_model= PedidoResponse)
def buscar_pedido(pedido_id: int, usuario_atual: dict = Depends(obter_usuario_atual)):
    usuario_id = int(usuario_atual.get("sub"))
    pedido = order_service.buscar_pedido(usuario_id, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )
    return pedido
    