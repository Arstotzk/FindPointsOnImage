import math
from PIL import ImageDraw
from PIL import Image
from config_read import Settings


class Point(object):

    def __init__(self, _name, _template, _guid):
        """
        Инициализация точки.
        :param _name: Имя.
        :param _template: Шаблон.
        """
        self.X = None
        self.Y = None
        self.name = _name
        self.template = _template
        self.templateWidth, self.templateHeight = self.template.size
        self.pointOnImage = None
        self.typeGuid = _guid
        self.guid = None

    def set_point_on_image(self, _image):
        """
        Поставить точку на изображение.
        :param _image: Изображение.
        """
        settings = Settings()
        self.pointOnImage = _image
        self.pointOnImage.putpixel((self.X, self.Y), (settings.colorR, settings.colorG, settings.colorB))
        img_draw = ImageDraw.Draw(self.pointOnImage)
        img_draw.text((self.X + settings.shift, self.Y + settings.shift), self.name,
                      (settings.colorR, settings.colorG, settings.colorB))

    def move(self, dx, dy):
        """
        Передвинуть точку.
        :param dx: Кол-во пикселей по x.
        :param dy: Кол-во пикселей по y.
        """
        self.X = self.X + dx
        self.Y = self.Y + dy

    def __str__(self):
        """
        Вывод координатов точки.
        :return: Строка с координатами.
        """
        return "Point(%s,%s)" % (self.X, self.Y)

    def get_x(self):
        """
        Получить координату x.
        :return: Координата x.
        """
        return self.X

    def get_y(self):
        """
        Получить координату y.
        :return: Координата y.
        """
        return self.Y

    def set_xy(self, _x, _y):
        """
        Установить координаты x,y.
        :param _x: Координата x.
        :param _y: Координата y.
        """
        self.X = _x
        self.Y = _y

    def distance(self, other):
        """
        Получить дистанцию между точками.
        :param other: Вторая точка.
        :return: Дистанция между точками.
        """
        dx = self.X - other.X
        dy = self.Y - other.Y
        return math.hypot(dx, dy)


class Points(object):

    def __init__(self):
        self.A = Point("A", Image.open("img/A.png").convert('L'), "4a5bebc2-0cee-4094-9c35-6400dbc97670")
        self.A1 = Point("A1", Image.open("img/A1.png").convert('L'), "023dfccf-f398-4961-89e6-ae906b83b550")
        self.ANS = Point("ANS", Image.open("img/ANS.png").convert('L'), "8d429c15-8bdf-4b8d-b79e-4263c8d0c9f5")
        self.AR = Point("AR", Image.open("img/AR.png").convert('L'), "6532698d-752d-42d0-a170-a279232d67ef")
        self.B = Point("B", Image.open("img/B.png").convert('L'), "b7fb5f16-a24d-4e64-8555-3a4b1b4e32f6")
        self.B1 = Point("B1", Image.open("img/B1.png").convert('L'), "e038ceb5-af53-47e9-a596-9a1c517760dd")
        self.BR = Point("BR", Image.open("img/BR.png").convert('L'), "ee5acf79-a6f1-4ca6-b391-7ca08b580926")
        self.DT = Point("DT", Image.open("img/DT.png").convert('L'), "8075743f-1be8-45b7-930c-de01e0292de9")
        self.En = Point("En", Image.open("img/En.png").convert('L'), "6c48f468-53f0-4043-b0b1-3044441a2258")
        self.Go = Point("Go", Image.open("img/Go.png").convert('L'), "acc34581-5925-472d-815c-c0aa450d9e52")
        self.Me = Point("Me", Image.open("img/Me.png").convert('L'), "3bdcf123-dc08-484e-a119-8023eefc0814")
        self.Mn = Point("Mn", Image.open("img/Mn.png").convert('L'), "ff2e65d9-1f50-44a6-b706-47d6e6ff974c")
        self.N = Point("N", Image.open("img/N.png").convert('L'), "01096d87-b09e-4d0d-bb88-32a9c4ca8288")
        self.Or = Point("Or", Image.open("img/Or.png").convert('L'), "4f302c4a-fa59-4542-b4b5-08e41eeb7192")
        self.PAC = Point("PAC", Image.open("img/PAC.png").convert('L'), "f00a7921-49a1-48a4-a5be-48c238bfc660")
        self.Pg = Point("Pg", Image.open("img/Pg.png").convert('L'), "d8c3357f-6f18-437d-a10d-bc4deff61eb7")
        self.PNS = Point("PNS", Image.open("img/PNS.png").convert('L'), "2393a6c8-e351-4bd1-b0da-c942a17cebb3")
        self.Po = Point("Po", Image.open("img/Po.png").convert('L'), "020f3e65-e88c-4c81-b9c4-a1c56fc8a06d")
        self.S = Point("S", Image.open("img/S.png").convert('L'), "d2d3a635-2ef2-4db2-a238-20d79129b97e")

        self.all = [self.A, self.A1, self.ANS, self.AR, self.B, self.B1, self.BR, self.DT, self.En, self.Go, self.Me,
                    self.Mn, self.N, self.Or, self.PAC, self.Pg, self.PNS, self.Po, self.S]
