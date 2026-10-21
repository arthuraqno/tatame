import os 
import pika
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

EXCHANGE = "tatame.eventos"

def publicar_evento(routing_key: str, mensagem: dict):
    credenciais = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    conexao = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credenciais)
    )
    canal = conexao.channel()
    canal.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    canal.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=json.dumps(mensagem),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    conexao.close()