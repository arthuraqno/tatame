# order-service

Pedidos de compra.

**Porta:** 8004 · **Armazenamento:** PostgreSQL (`order_db`, tabelas `pedidos` e `itens_pedido`)

## Rotas (todas exigem JWT)

| Método | Rota | O que faz |
|---|---|---|
| POST | `/pedidos` | Cria um pedido a partir do carrinho do usuário |
| GET | `/pedidos` | Lista os pedidos do usuário, do mais recente ao mais antigo |
| GET | `/pedidos/{id}` | Detalha um pedido (só se for do próprio usuário) |

## Eventos

- **Consome** `pagamento.confirmado` (fila `order.pagamento_confirmado`) pelo `order-consumer`, que roda em um container próprio, e marca o pedido como `pago`.
- **Publica** `pedido.pago` (`pedido_id`, `usuario_id` e os itens com `produto_id` e `quantidade`) logo depois.

## Detalhes

- **Preço congelado:** o pedido guarda o preço e o nome de cada item no momento da compra. Mudanças posteriores no catálogo não alteram pedidos antigos.
- O pedido e seus itens são gravados numa única transação. Depois do commit, o carrinho é esvaziado no `cart-service`; se essa chamada falhar, o pedido continua salvo.
- Consultar um pedido de outro usuário responde `404`, sem revelar que ele existe.
- O pedido só muda de `pendente` para `pago` uma vez, então um evento repetido não tem efeito.

## Variáveis de ambiente

`DATABASE_URL`, `CART_SERVICE_URL`, `RABBITMQ_HOST`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`. A `public_key.pem` é montada como volume.
