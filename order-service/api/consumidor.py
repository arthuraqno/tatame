import json
import pika
from mensageria import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD, EXCHANGE, publicar_evento
from services.order_service import OrderService

FILA = "order.pagamento_confirmado"
CHAVE = "pagamento.confirmado"

order_service = OrderService()


def tratar_pagamento_confirmado(canal, metodo, propriedades, corpo):
    dados = json.loads(corpo)
    resultado = order_service.marcar_como_pago(dados["pedido_id"])
    if resultado is None:
        print(f"Pedido {dados['pedido_id']} não encontrado")
    else:
        publicar_evento("pedido.pago", resultado)
        print(f"Pedido {dados['pedido_id']} marcado como pago")
    canal.basic_ack(delivery_tag=metodo.delivery_tag)


def iniciar():
    credenciais = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    conexao = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credenciais)
    )
    canal = conexao.channel()
    canal.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    canal.queue_declare(queue=FILA, durable=True)
    canal.queue_bind(queue=FILA, exchange=EXCHANGE, routing_key=CHAVE)
    canal.basic_qos(prefetch_count=1)
    canal.basic_consume(queue=FILA, on_message_callback=tratar_pagamento_confirmado)
    print("Aguardando avisos...")
    canal.start_consuming()


if __name__ == "__main__":
    iniciar()