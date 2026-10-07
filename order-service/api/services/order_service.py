import httpx
import os
from schemas.pedido import ItemPedidoResponse, PedidoResponse
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from dotenv import load_dotenv
from decimal import Decimal
from sqlalchemy.orm import Session
from database import engine

load_dotenv()

CART_SERVICE_URL = os.getenv("CART_SERVICE_URL")
class OrderService:
    def _buscar_carrinho(self, token : str):
        resposta = httpx.get(f"{CART_SERVICE_URL}/carrinho", headers={"Authorization": f"Bearer {token}"})
        if resposta.status_code != 200:
            return None
        return resposta.json()

    def _limpar_carrinho(self, token: str):
        try:
            httpx.delete(
                f"{CART_SERVICE_URL}/carrinho",
                headers={"Authorization": f"Bearer {token}"}
            )
        except httpx.HTTPError:
            pass

    def criar_pedido(self, usuario_id : int, token : str):
        carrinho = self._buscar_carrinho(token)
        if carrinho is None:
            return None
        if not carrinho["itens"]:
            return None

        with Session(engine) as session:
            pedido = Pedido(
                usuario_id = usuario_id,
                total = Decimal(carrinho["total"]))
            session.add(pedido)
            session.flush()

            itens_criados = []

            for item in carrinho["itens"]:
                item_pedido = ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=item["produto_id"],
                    quantidade=item["quantidade"],
                    preco_unitario=Decimal(item["preco"]),
                    nome_produto=item["nome"]
                )
                session.add(item_pedido)
                itens_criados.append(item_pedido)

            session.commit()
            self._limpar_carrinho(token)
            return self._to_response(pedido, itens_criados)

    def _to_response(self, pedido: Pedido, itens: list[ItemPedido]) -> PedidoResponse:
        lista_itens = []

        for item in itens:
            item_response = ItemPedidoResponse(
                produto_id=item.produto_id,
                nome_produto=item.nome_produto,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario,
                subtotal=item.preco_unitario * item.quantidade
            )
            lista_itens.append(item_response)

        return PedidoResponse(
            id=pedido.id,
            status=pedido.status,
            total=pedido.total,
            criado_em=pedido.criado_em,
            itens=lista_itens
        )