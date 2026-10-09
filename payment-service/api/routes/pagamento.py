from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.pagamento import PagamentoResponse, PagamentoCreate
from services.pagamento_service import PagamentoService
from auth import obter_usuario_atual

router = APIRouter()
pagamento_service = PagamentoService()
security_scheme = HTTPBearer()

@router.post("/pagamentos", response_model=PagamentoResponse)
def criar_pagamento(
    dados: PagamentoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    usuario_atual: dict = Depends(obter_usuario_atual)):

    usuario_id = int(usuario_atual.get("sub"))
    token = credentials.credentials
    pagamento = pagamento_service.criar_pagamento(dados.pedido_id, usuario_id, token)
    if pagamento is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pedido não encontrado ou não está pendente"
        )
    return pagamento

