from b_rabbit import BRabbit
import time
from config_read import Settings

settings = Settings()
rabbit = BRabbit(host=settings.rabbitHost, port=settings.rabbitPort,
                 user=settings.rabbitLogin, password=settings.rabbitPassword,
                 vhost=settings.rabbitVirtualHost)


def taskListener(server, body):
    print('Task Request received')
    print(str(body))
    time.sleep(5)
    server.send_return(payload="return this value to requester")


#publisher = rabbit.EventPublisher(b_rabbit=rabbit,
#                                  publisher_name='main').publish(routing_key='processing_images',
#                                                                payload='Hello from publisher')

taskExecuter = rabbit.TaskExecutor(
                                    b_rabbit=rabbit,
                                    routing_key='processing_images',
                                    executor_name='mainExchange',
                                    task_listener=taskListener)

taskExecuter.run_task_on_thread()