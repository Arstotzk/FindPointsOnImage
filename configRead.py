import yaml

class Settings:

    def __init__(self):
        """
        Инициализация настроек
        """
        config = self.readYaml("config.yaml")
        self.threadsCPU = config["threadsCPU"]
        self.threadNums = config["threadNums"]
        self.multipleResize = config["multipleResize"]
        self.processingSize = config["processingSize"]
        self.processingSizeHalf = int(config["processingSize"]/2)

        self.colorR = config["colorR"]
        self.colorG = config["colorG"]
        self.colorB = config["colorB"]
        self.shift = config["shift"]

    def readYaml(self, filePath):
        """
        Получить параметры из config.yaml.
        :param filePath: Путь до config.yaml.
        :return: Параметры из config.yaml.
        """
        with open(filePath, "r") as file:
            return yaml.safe_load(file)