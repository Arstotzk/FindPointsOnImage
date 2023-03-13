import math
from PIL import ImageDraw
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
