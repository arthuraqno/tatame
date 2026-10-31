# product-service

Catálogo de artigos de jiu-jitsu (kimonos, faixas, acessórios).

**Porta:** 8002 · **Armazenamento:** PostgreSQL (`product_db`)

## Rotas

| Método | Rota | Acesso | O que faz |
|---|---|---|---|
| GET | `/produtos` | público | Lista os produtos |
| GET | `/produtos/{id}` | público | Detalha um produto |
| POST | `/produtos` | admin | Cadastra um produto |
| PUT | `/produtos/{id}` | admin | Atualiza um produto |
| DELETE | `/produtos/{id}` | admin | Desativa um produto |

## Eventos

- **Consome** `pedido.pago` (fila `product.pedido_pago`) pelo `product-consumer`, que roda em um container próprio com o mesmo código, e baixa o estoque de cada item.

## Detalhes

- **Soft delete:** apagar um produto só marca `ativo = false`, para não quebrar pedidos antigos que apontam para ele.
- **Baixa de estoque idempotente:** cada pedido tratado é registrado na tabela `pedidos_processados`, com `pedido_id` único. Um evento repetido é ignorado, e a baixa de todos os itens e o registro do pedido acontecem num único commit.
- Se o estoque ficar negativo (duas pessoas pagaram pela última unidade), a baixa acontece mesmo assim e um aviso vai para o log: o dinheiro já entrou.
- O papel de admin é lido do próprio JWT, validado com a chave pública.

## Variáveis de ambiente

`DATABASE_URL`, `RABBITMQ_HOST`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`. A `public_key.pem` é montada como volume.
