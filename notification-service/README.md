# notification-service

Notificações aos clientes. Não tem API: é só um consumidor de eventos.

**Armazenamento:** PostgreSQL (`notification_db`, tabela `contatos`)

## Eventos

| Fila | Evento | O que faz |
|---|---|---|
| `notification.usuario_criado` | `usuario.criado` | Guarda o contato (`usuario_id`, e-mail e telefone) |
| `notification.pedido_pago` | `pedido.pago` | Busca o contato e monta o e-mail de confirmação |

## Detalhes

- **Não chama o `user-service`.** Ele mantém a própria cópia dos contatos, recebida por eventos.
- **Uma falha aqui não derruba uma venda.** Se o serviço estiver fora do ar, o pedido é pago e o estoque é baixado normalmente; os eventos esperam na fila e são tratados quando ele volta.
- Se o contato de um usuário não existir (por exemplo, um usuário criado antes deste serviço), o motivo vai para o log e o evento é confirmado, sem travar a fila.
- O contato tem `usuario_id` único, então um `usuario.criado` repetido não duplica nada.
- **Envio simulado:** a mensagem é registrada no log. O envio por um provedor de e-mail fica para uma próxima versão.

## Variáveis de ambiente

`DATABASE_URL`, `RABBITMQ_HOST`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`.
