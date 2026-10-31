# cart-service

Carrinho de compras de cada usuário.

**Porta:** 8003 · **Armazenamento:** Redis (`cart:{usuario_id}`, um hash de `produto_id` para quantidade)

## Rotas (todas exigem JWT)

| Método | Rota | O que faz |
|---|---|---|
| GET | `/carrinho` | Mostra o carrinho com preço, subtotal e total |
| POST | `/carrinho/itens` | Adiciona um produto (soma à quantidade que já existe) |
| PUT | `/carrinho/itens/{produto_id}` | Define a quantidade exata de um item |
| DELETE | `/carrinho/itens/{produto_id}` | Remove um item |
| DELETE | `/carrinho` | Esvazia o carrinho |

## Comunicação

- **Chama o `product-service`** por HTTP para conferir se o produto existe e se há estoque, e para mostrar o preço atual.
- É chamado pelo `order-service`, que lê o carrinho para montar o pedido e depois o esvazia.

## Detalhes

- O carrinho guarda só o número do produto e a quantidade. Nome e preço vêm do catálogo a cada consulta, então o carrinho sempre mostra o preço vigente.
- O dono do carrinho vem do JWT, nunca do corpo da requisição.

## Variáveis de ambiente

`REDIS_URL`, `PRODUCT_SERVICE_URL`. A `public_key.pem` é montada como volume.
