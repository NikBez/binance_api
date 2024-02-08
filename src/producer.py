import pika
import json


async def run(client):

    result = await client.test_book_ticker('EURUSDT')

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(result, ensure_ascii=True))
    print(f" [x] Sent: {result}")

    connection.close()