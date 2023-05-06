import pika
from config_read import Settings
from PIL import Image
from normalization import Normalization
from image_operations import ImageOperations
from b_rabbit import BRabbit


def callback(server, body):
    try:
        body_str = body.decode("utf-8")
        print("Start guid: " + body_str)

        settings = Settings()
        imagePath = settings.filePath + '\\' + body_str
        image = Image.open(imagePath)
        #norm = Normalization(image)
        #norm.normalize()
        imageOper = ImageOperations(image, settings)
        print("Normalization complete guid: " + body_str)
        imageOper.find_points_by_template()
        print("Points founded guid: " + body_str)
        imageOper.find_cephalometric_params()
        print("Params founded guid: " + body_str)
        imageOper.put_cephalometric_point_and_params(body_str)
        print("Image guid: " + body_str + " Executing time: " + str(imageOper.execution_time()))
        imageOper.print_cephalometric_params()

        server.send_return(payload="return this value to requester")
        print("End guid: " + body_str)
    except Exception as e:
        print("Image guid:" + body_str + " Error: " + str(e))
    return

def callbackFindParams(server, body):
    try:
        body_str = body.decode("utf-8")
        print("Start guid: " + body_str)
        settings = Settings()
        imagePath = settings.filePath + '\\' + body_str
        image = Image.open(imagePath)
        imageOper = ImageOperations(image, settings)
        imageOper.get_cephalometric_points(body_str)
        imageOper.get_cephalometric_lines(body_str)
        imageOper.get_cephalometric_params(body_str)
        print("Points got guid: " + body_str)
        imageOper.find_cephalometric_params()
        print("Params founded guid: " + body_str)
        imageOper.update_cephalometric_point_and_params(body_str)
        imageOper.print_cephalometric_params()

        server.send_return(payload="return this value to requester")
        print("End guid: " + body_str)
    except Exception as e:
        print("Image guid:" + body_str + " Error: " + str(e))
    return

def callbackTest(server, body):
    print('Task Request received')
    body_str = body.decode("utf-8")
    print(body_str)
    server.send_return(payload="return this value to requester")


class Rabbit:
    def __init__(self):
        settings = Settings()

        self.brabbit = BRabbit(host=settings.rabbitHost, port=settings.rabbitPort,
                               user=settings.rabbitLogin, password=settings.rabbitPassword,
                               vhost=settings.rabbitVirtualHost)

        self.subscriber = self.brabbit.TaskExecutor(
                                    b_rabbit=self.brabbit,
                                    routing_key='processing_images',
                                    executor_name='mainExchange',
                                    task_listener=callback)

        self.subscriberFindParams = self.brabbit.TaskExecutor(
                                    b_rabbit=self.brabbit,
                                    routing_key='find_params_images',
                                    executor_name='mainExchange',
                                    task_listener=callbackFindParams)

        self.subscriber.run_task_on_thread()

        self.subscriberFindParams.run_task_on_thread()


