import math
from PIL import ImageDraw
from PIL import Image
from config_read import Settings


class Point(object):

    def __init__(self, _name, _template):
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
        self.A = Point("A", Image.open("img/A.png").convert('L'))
        self.A1 = Point("A1", Image.open("img/A1.png").convert('L'))
        self.ANS = Point("ANS", Image.open("img/ANS.png").convert('L'))
        self.AR = Point("AR", Image.open("img/AR.png").convert('L'))
        self.B = Point("B", Image.open("img/B.png").convert('L'))
        self.B1 = Point("B1", Image.open("img/B1.png").convert('L'))
        self.BR = Point("BR", Image.open("img/BR.png").convert('L'))
        self.DT = Point("DT", Image.open("img/DT.png").convert('L'))
        self.En = Point("En", Image.open("img/En.png").convert('L'))
        self.Go = Point("Go", Image.open("img/Go.png").convert('L'))
        self.Me = Point("Me", Image.open("img/Me.png").convert('L'))
        self.Mn = Point("Mn", Image.open("img/Mn.png").convert('L'))
        self.N = Point("N", Image.open("img/N.png").convert('L'))
        self.Or = Point("Or", Image.open("img/Or.png").convert('L'))
        self.PAC = Point("PAC", Image.open("img/PAC.png").convert('L'))
        self.Pg = Point("Pg", Image.open("img/Pg.png").convert('L'))
        self.PNS = Point("PNS", Image.open("img/PNS.png").convert('L'))
        self.Po = Point("Po", Image.open("img/Po.png").convert('L'))
        self.S = Point("S", Image.open("img/S.png").convert('L'))

        self.all = [self.A, self.A1, self.ANS, self.AR, self.B, self.B1, self.BR, self.DT, self.En, self.Go, self.Me,
                    self.Mn, self.N, self.Or, self.PAC, self.Pg, self.PNS, self.Po, self.S]
