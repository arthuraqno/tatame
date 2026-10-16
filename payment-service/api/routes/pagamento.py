import os
import stripe
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.pagamento import PagamentoResponse, PagamentoCreate
from services.pagamento_service import PagamentoService
from mensageria import publicar_evento
from auth import obter_usuario_atual
from dotenv import load_dotenv

load_dotenv()

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

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

@router.post("/pagamentos/webhook")
async def webhook_stripe(request: Request):
    payload = await request.body()
    assinatura = request.headers.get("stripe-signature")

    try:
        evento = stripe.Webhook.construct_event(payload, assinatura, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.SignatureVerificationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assinatura inválida")

    if evento.type == "checkout.session.completed":
        sessao = evento.data.object
        if sessao.payment_status == "paid":
            pedido_id = pagamento_service.marcar_como_pago(sessao.id)
            if pedido_id is not None:
                publicar_evento("pagamento.confirmado", {"pedido_id": pedido_id})

    return {"recebido": True}
