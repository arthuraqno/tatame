import httpx
import os
from decimal import Decimal
from schemas.carrinho import CarrinhoResponse, ItemCarrinho
from dotenv import load_dotenv
from redis_client import redis_client

load_dotenv()
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")

class CarrinhoService:
    def _buscar_produto(self, produto_id: int):
        resposta = httpx.get(f"{PRODUCT_SERVICE_URL}/produtos/{produto_id}")
        if resposta.status_code != 200:
            return None
        return resposta.json()

    def adcionar_item(self, usuario_id, produto_id, quantidade):
        chave = f"cart:{usuario_id}"
        produto = self._buscar_produto(produto_id)
        if produto is None:
            return None

        quantidade_atual = redis_client.hget(chave, str(produto_id))
        if quantidade_atual is None:
            quantidade_atual = 0
        else:
            quantidade_atual = int(quantidade_atual)

        quantidade_total = quantidade_atual + quantidade

        if produto["estoque"] < quantidade_total:
            return None

        redis_client.hset(chave, str(produto_id), quantidade_total)
        return True

    def ver_carrinho(self, usuario_id: int):
        chave = f"cart:{usuario_id}"
        itens_redis = redis_client.hgetall(chave)
        lista_itens = []
        total = Decimal(0)

        for produto_id_str, quantidade_str in itens_redis.items():
            produto = self._buscar_produto(int(produto_id_str))
            if produto is None:
                continue

            quantidade = int(quantidade_str)
            preco = Decimal(produto["preco"])
            subtotal = preco * quantidade

            item = ItemCarrinho(
                produto_id=produto["id"],
                nome=produto["nome"],
                preco=preco,
                quantidade=quantidade,
                subtotal=subtotal
            )
            lista_itens.append(item)
            total += subtotal

        return CarrinhoResponse(itens=lista_itens, total=total)

    def atualizar_quantidade(self,usuario_id, produto_id: int, quantidade: int):
        chave = f"cart:{usuario_id}"
        produto = self._buscar_produto(produto_id)
        if produto is None:
            return None
        
        if produto["estoque"] < quantidade:
            return None

        redis_client.hset(chave, str(produto_id), quantidade)
        return True

    def remover_item(self, usuario_id: int, produto_id: int):
        chave = f"cart:{usuario_id}"
        resultado = redis_client.hdel(chave, str(produto_id))
        return resultado > 0