import pika
from config_read import Settings


def callback(ch, method, properties, body):
    body_str = body.decode("utf-8")
    print("Start " + body_str)
    #TODO Добавить обработку изображения
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("End")
    return


class Rabbit:
    def __init__(self):
        settings = Settings()
        self.parameters = pika.URLParameters('amqp://' + settings.rabbitLogin + ':' + settings.rabbitPassword + '@' +
                                             settings.rabbitHost + ':' + str(settings.rabbitPort) + '/' +
                                             settings.rabbitVirtualHost)
        self.parameters.socket_timeout = 5
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='processing_images')

