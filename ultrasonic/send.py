import pika, os

def send_message():
    url = 'amqps://vdwwsmtz:8t1_gM675-qlXqIZ70C4lA5gQyZTTnpR@crow.rmq.cloudamqp.com/vdwwsmtz'
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='hello') # Declare a queue
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello CloudAMQP!')

    connection.close()