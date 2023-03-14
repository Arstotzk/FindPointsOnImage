import numpy as np
from PIL import Image
import time
import thread_calc
from point import Points
from vector import Lines
from cephalometric_params import Params

np.set_printoptions(threshold=np.inf)


class ImageOperations:

    def __init__(self, _image, _setting):
        """
        Инициализация класса в котором выполняется обработка изображения.
        :param _image: Изображение.
        :param _setting: Настройки из конфига.
        """
        self.setting = _setting
        self.startTime = None
        self.endTime = None
        self.difTime = None
        self.image = _image
        self.resizedImage = self.resize_img(self.image, self.setting.multipleResize)
        self.width, self.height = self.image.size
        self.arrSumFull = np.full((self.width, self.height), 0)
        # Точки
        self.points = Points()
        # Линии
        self.lines = Lines()
        # Параметры
        self.params = Params()

    def execution_time(self):
        """
        Возвращает время затраченое на обработку изображения.
        :return: Время в мс.
        """
        return self.endTime - self.startTime

    def set_points_on_image(self):
        """
        Ставит на изображение найденные точки.
        """
        self.points.A.set_point_on_image(self.image)
        self.points.A1.set_point_on_image(self.image)
        self.points.ANS.set_point_on_image(self.image)
        self.points.AR.set_point_on_image(self.image)
        self.points.B.set_point_on_image(self.image)
        self.points.B1.set_point_on_image(self.image)
        self.points.BR.set_point_on_image(self.image)
        self.points.DT.set_point_on_image(self.image)
        self.points.En.set_point_on_image(self.image)
        self.points.Go.set_point_on_image(self.image)
        self.points.Me.set_point_on_image(self.image)
        self.points.Mn.set_point_on_image(self.image)
        self.points.N.set_point_on_image(self.image)
        self.points.Or.set_point_on_image(self.image)
        self.points.PAC.set_point_on_image(self.image)
        self.points.Pg.set_point_on_image(self.image)
        self.points.PNS.set_point_on_image(self.image)
        self.points.Po.set_point_on_image(self.image)
        self.points.S.set_point_on_image(self.image)

    def resize_img(self, _img, multiple):
        """
        Уменьшение изображение.
        :param _img: Исходное изображение.
        :param multiple: Коэффициент уменьшения.
        :return:
        """
        width, height = _img.size
        new_width = int(width / multiple)
        new_height = int(height / multiple)
        _img = _img.resize((new_width, new_height), Image.ANTIALIAS)
        return _img

    def find_points_by_template(self):
        """
        Найти точки по шаблону.
        """
        self.startTime = int(round(time.time() * 1000))
        img_full = self.image.copy()
        img_full = img_full.convert('L')

        self.find_point_by_template(img_full, self.points.A.template, self.points.A)
        self.find_point_by_template(img_full, self.points.A1.template, self.points.A1)
        self.find_point_by_template(img_full, self.points.ANS.template, self.points.ANS)
        self.find_point_by_template(img_full, self.points.AR.template, self.points.AR)
        self.find_point_by_template(img_full, self.points.B.template, self.points.B)
        self.find_point_by_template(img_full, self.points.B1.template, self.points.B1)
        self.find_point_by_template(img_full, self.points.BR.template, self.points.BR)
        self.find_point_by_template(img_full, self.points.DT.template, self.points.DT)
        self.find_point_by_template(img_full, self.points.En.template, self.points.En)
        self.find_point_by_template(img_full, self.points.Go.template, self.points.Go)
        self.find_point_by_template(img_full, self.points.Me.template, self.points.Me)
        self.find_point_by_template(img_full, self.points.Mn.template, self.points.Mn)
        self.find_point_by_template(img_full, self.points.N.template, self.points.N)
        self.find_point_by_template(img_full, self.points.Or.template, self.points.Or)
        self.find_point_by_template(img_full, self.points.PAC.template, self.points.PAC)
        self.find_point_by_template(img_full, self.points.Pg.template, self.points.Pg)
        self.find_point_by_template(img_full, self.points.PNS.template, self.points.PNS)
        self.find_point_by_template(img_full, self.points.Po.template, self.points.Po)
        self.find_point_by_template(img_full, self.points.S.template, self.points.S)

        self.endTime = int(round(time.time() * 1000))

    def find_point_by_template(self, _img_full, _template_full, _point):
        """
        Нахождение точки по шаблону.
        :param _img_full: Изображение.
        :param _template_full: Шаблон.
        :param _point: Точка.
        """
        resized_img = self.resizedImage
        resized_img = resized_img.convert('L')
        template = _template_full
        template = template.convert('L')
        template = self.resize_img(template, self.setting.multipleResize)
        width, height = resized_img.size
        width_template, height_template = template.size
        half_size_template = int(width_template / 2)
        array_sum = np.full((width, height), 0)

        sum_old = 0
        for x in range(half_size_template, width - (half_size_template)):
            for y in range(half_size_template, height - (half_size_template)):
                sum = thread_calc.calc_sum(x, y, resized_img, template, half_size_template)
                array_sum[x, y] = sum
                if (sum > sum_old):
                    sum_old = sum
                    x_point = x
                    y_point = y
            # print("Ready resize: " + str(((x - half_size_template + 1) / (width - width_template)) * 100) + "%")

        print(x_point, y_point)

        x_point_full = x_point * self.setting.multipleResize
        y_point_full = y_point * self.setting.multipleResize
        print(x_point_full, y_point_full)

        x_point_th = x_point_full - self.setting.processingSizeHalf
        y_point_th = y_point_full - self.setting.processingSizeHalf

        arr_sum_full = thread_calc.start(x_point_th, y_point_th, _img_full, _template_full, self.setting.threadNums,
                                         self.setting.processingSize)
        print("Потоки завершены")

        max_array_sum = 0
        for x in range(x_point_full - self.setting.processingSizeHalf, x_point_full + self.setting.processingSizeHalf):
            for y in range(y_point_full - self.setting.processingSizeHalf,
                           y_point_full + self.setting.processingSizeHalf):
                next_array_sum = arr_sum_full[
                    x - x_point_full + self.setting.processingSizeHalf, y - y_point_full + self.setting.processingSizeHalf]
                if next_array_sum > max_array_sum:
                    max_array_sum = next_array_sum
                    _point.X = x
                    _point.Y = y

        # self.show_found_gradient(arr_sum_full, x_point_full, y_point_full, _imgFull)

    def show_found_gradient(self, _arr_sum_full, _x_point_full, _y_point_full, _img_full):
        """
        Для отладки, показывает изображение с градиентом вероятности нахождения точки
        :param _arr_sum_full: Массив с вероятностью нахождения точки
        :param _x_point_full: X координата области обработки
        :param _y_point_full: Y координата области обработки
        :param _img_full: Исходное изображение
        """
        # Отображение градиента нахождения точки
        max_int = _arr_sum_full.max()
        for x in range(_x_point_full - self.setting.processingSizeHalf,
                       _x_point_full + self.setting.processingSizeHalf):
            for y in range(_y_point_full - self.setting.processingSizeHalf,
                           _y_point_full + self.setting.processingSizeHalf):
                color = int(((_arr_sum_full[
                    x - _x_point_full + self.setting.processingSizeHalf, y - _y_point_full + self.setting.processingSizeHalf]) / max_int) * 255)
                _img_full.putpixel((x, y), color)
        _img_full.show()

    def find_cephalometric_params(self):
        # Расчет линий
        self.lines.calculate(self.points)

        # Расчет параметров
        self.params.calculate(self.points, self.lines)

    def print_cephalometric_params(self):

        for line in self.lines.all:
            print(line.name, line.X, line.Y)

        for param in self.params.all:
            if param.isFound:
                print(param.name, param.value, param.isNormal)
