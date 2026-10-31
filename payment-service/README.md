# payment-service

Pagamentos com o Stripe, em modo de teste.

**Porta:** 8005 · **Armazenamento:** PostgreSQL (`payment_db`)

## Rotas

| Método | Rota | Acesso | O que faz |
|---|---|---|---|
| POST | `/pagamentos` | JWT | Cria uma sessão de checkout no Stripe e devolve o link de pagamento |
| POST | `/pagamentos/webhook` | assinatura do Stripe | Recebe o aviso de pagamento concluído |

## Eventos

- **Publica** `pagamento.confirmado` (`pedido_id`) quando o Stripe confirma o pagamento.

## Detalhes

- **O valor nunca vem do cliente.** O cliente informa só o `pedido_id`; o serviço consulta o pedido no `order-service`, com o token do próprio cliente, e cobra o total que está lá. Só pedidos `pendentes` podem ser pagos.
- **O cartão nunca passa pelo Tatame.** O pagamento acontece na página do Stripe.
- **Webhook assinado.** O corpo da requisição é lido cru e a assinatura é conferida com o segredo do webhook. Uma requisição sem assinatura válida responde `400`.
- **Idempotência.** Um aviso repetido do Stripe não muda o que já está pago. O evento é publicado de novo, e quem consome ignora o que já tratou.

## Variáveis de ambiente

`DATABASE_URL`, `ORDER_SERVICE_URL`, `RABBITMQ_HOST`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`. A `public_key.pem` é montada como volume.

Para receber o webhook localmente:

```bash
stripe listen --events checkout.session.completed --forward-to localhost:8005/pagamentos/webhook
```
