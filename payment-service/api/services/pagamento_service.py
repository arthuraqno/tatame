import httpx
import os
import stripe
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import engine
from schemas.pagamento import PagamentoCreate, PagamentoResponse
from models.pagamento import Pagamento
from decimal import Decimal

load_dotenv()

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

stripe_client = stripe.StripeClient(STRIPE_SECRET_KEY)

class PagamentoService:
    def _buscar_pedido(self, pedido_id: int, token: str):
        resposta = httpx.get(f"{ORDER_SERVICE_URL}/pedidos/{pedido_id}", headers={"Authorization": f"Bearer {token}"})
        if resposta.status_code != 200:
            return None
        return resposta.json()

    def _criar_sessao_stripe(self, pedido_id: int, valor: Decimal):
        sessao = stripe_client.v1.checkout.sessions.create({
            "mode": "payment",
            "success_url": "http://localhost:8005/sucesso",
            "cancel_url": "http://localhost:8005/cancelado",
            "client_reference_id": str(pedido_id),
            "line_items": [{
                "quantity": 1,
                "price_data": {
                    "currency": "brl",
                    "unit_amount": int(valor * 100),
                    "product_data": {"name": f"Pedido #{pedido_id} - Tatame"},
                },
            }],
        })
        return sessao

    def criar_pagamento(self, pedido_id:int, usuario_id: int, token: str):
        pedido = self._buscar_pedido(pedido_id, token)
        if pedido is None:
            return None
        if pedido["status"] != "pendente":
            return None

        valor = Decimal(pedido["total"])
        sessao = self._criar_sessao_stripe(pedido_id, valor)

        with Session(engine) as session:
            pagamento = Pagamento(pedido_id = pedido_id,
                                  usuario_id = usuario_id, 
                                  valor = valor, 
                                  stripe_session_id = sessao.id)
            session.add(pagamento)
            session.commit()
            session.refresh(pagamento)
            return self._to_response(pagamento, sessao.url)

    def _to_response(self, pagamento: Pagamento, checkout_url) -> PagamentoResponse:
        return PagamentoResponse(
            id=pagamento.id,
            pedido_id=pagamento.pedido_id,
            valor=pagamento.valor,
            status=pagamento.status,
            checkout_url=checkout_url)