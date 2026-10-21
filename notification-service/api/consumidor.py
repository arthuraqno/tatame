import json
import pika
from mensageria import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD, EXCHANGE
from services.notificacao_service import NotificationService

FILA_CONTATOS = "notification.usuario_criado"
CHAVE_CONTATOS = "usuario.criado"
FILA_PEDIDOS = "notification.pedido_pago"
CHAVE_PEDIDOS = "pedido.pago"

notification_service = NotificationService()

def tratar_usuario_criado(canal, metodo, propriedades, corpo):
    dados = json.loads(corpo)
    guardou = notification_service.guardar_contato(dados["usuario_id"], dados["email"], dados["telefone"])
    if guardou:
        print(f"Contato do usuário {dados['usuario_id']} guardado")
    else:
        print(f"Contato do usuário {dados['usuario_id']} já existia")
    canal.basic_ack(delivery_tag=metodo.delivery_tag)

def tratar_pedido_pago(canal, metodo, propriedades, corpo):
    dados = json.loads(corpo)
    resultado = notification_service.montar_mensagem(dados)
    if resultado is not None:
        print(f"Enviando e-mail para {resultado['para']} | Assunto: {resultado['assunto']} | {resultado['texto']}")
    canal.basic_ack(delivery_tag=metodo.delivery_tag)

def iniciar():
    credenciais = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    conexao = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credenciais)
    )
    canal = conexao.channel()
    canal.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    canal.queue_declare(queue=FILA_CONTATOS, durable=True)
    canal.queue_bind(queue=FILA_CONTATOS, exchange=EXCHANGE, routing_key=CHAVE_CONTATOS)
    canal.queue_declare(queue=FILA_PEDIDOS, durable=True)
    canal.queue_bind(queue=FILA_PEDIDOS, exchange=EXCHANGE, routing_key=CHAVE_PEDIDOS)
    canal.basic_qos(prefetch_count=1)
    canal.basic_consume(queue=FILA_CONTATOS, on_message_callback=tratar_usuario_criado)
    canal.basic_consume(queue=FILA_PEDIDOS, on_message_callback=tratar_pedido_pago)
    print("Aguardando avisos...")
    canal.start_consuming()


if __name__ == "__main__":
    iniciar()