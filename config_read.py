import yaml


class Settings:

    def __init__(self):
        """
        Инициализация настроек
        """
        config = self.read_yaml("config.yaml")
        self.threadsCPU = config["threadsCPU"]
        self.threadNums = config["threadNums"]
        self.multipleResize = config["multipleResize"]
        self.processingSize = config["processingSize"]
        self.processingSizeHalf = int(config["processingSize"] / 2)

        self.colorR = config["colorR"]
        self.colorG = config["colorG"]
        self.colorB = config["colorB"]
        self.shift = config["shift"]

    def read_yaml(self, _file_path):
        """
        Получить параметры из config.yaml.
        :param _file_path: Путь до config.yaml.
        :return: Параметры из config.yaml.
        """
        with open(_file_path, "r") as file:
            return yaml.safe_load(file)
