import yaml

class Settings:

    def __init__(self):
        config = self.readYaml("config.yaml")
        self.threadsCPU = config["threadsCPU"]
        self.threadNums = config["threadNums"]
        self.multipleResize = config["multipleResize"]
        self.processingSize = config["processingSize"]
        self.processingSizeHalf = int(config["processingSize"]/2)

    def readYaml(self, filePath):
        with open(filePath, "r") as file:
            return yaml.safe_load(file)