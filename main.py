from rabbit import Rabbit
import rabbit

rabbit_obj = Rabbit()
rabbit_obj.channel.basic_consume("processing_images", rabbit.callback)
rabbit_obj.channel.start_consuming()
rabbit_obj.connection.close()

