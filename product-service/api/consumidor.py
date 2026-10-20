import json
import pika
from mensageria import RABBITMQ_HOST, RABBITMQ_PASSWORD,  RABBITMQ_USER, EXCHANGE, publicar_evento
from services.produto_service import ProdutoService

FILA = "product.pedido_pago"
CHAVE = "pedido.pago"

produto_service = ProdutoService()

def tratar_pedido_pago(canal, metodo, propriedades, corpo):
    dados = json.loads(corpo)
    baixou = produto_service.baixar_estoque(dados["pedido_id"], dados["itens"])
    if baixou:
        print(f"Estoque baixado para o pedido {dados['pedido_id']}")
    else:
        print(f"Pedido {dados['pedido_id']} já tinha sido tratado")
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
    canal.basic_consume(queue=FILA, on_message_callback=tratar_pedido_pago)
    print("Aguardando avisos...")
    canal.start_consuming()


if __name__ == "__main__":
    iniciar()