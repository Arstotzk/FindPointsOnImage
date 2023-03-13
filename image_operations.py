import numpy as np
from PIL import Image
import time
import thread_culc
from point import Point

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
        self.O = Point("O", Image.open("img/O.png").convert('L'))
        self.PAC = Point("PAC", Image.open("img/PAC.png").convert('L'))
        self.Pg = Point("Pg", Image.open("img/Pg.png").convert('L'))
        self.PNS = Point("PNS", Image.open("img/PNS.png").convert('L'))
        self.Pr = Point("Pr", Image.open("img/Pr.png").convert('L'))

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
        self.A.set_point_on_image(self.image)
        self.A1.set_point_on_image(self.image)
        self.ANS.set_point_on_image(self.image)
        self.AR.set_point_on_image(self.image)
        self.B.set_point_on_image(self.image)
        self.B1.set_point_on_image(self.image)
        self.BR.set_point_on_image(self.image)
        self.DT.set_point_on_image(self.image)
        self.En.set_point_on_image(self.image)
        self.Go.set_point_on_image(self.image)
        self.Me.set_point_on_image(self.image)
        self.Mn.set_point_on_image(self.image)
        self.N.set_point_on_image(self.image)
        self.O.set_point_on_image(self.image)
        self.PAC.set_point_on_image(self.image)
        self.Pg.set_point_on_image(self.image)
        self.PNS.set_point_on_image(self.image)
        self.Pr.set_point_on_image(self.image)

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

        self.find_point_by_template(img_full, self.A.template, self.A)
        self.find_point_by_template(img_full, self.A1.template, self.A1)
        self.find_point_by_template(img_full, self.ANS.template, self.ANS)
        self.find_point_by_template(img_full, self.AR.template, self.AR)
        self.find_point_by_template(img_full, self.B.template, self.B)
        self.find_point_by_template(img_full, self.B1.template, self.B1)
        self.find_point_by_template(img_full, self.BR.template, self.BR)
        self.find_point_by_template(img_full, self.DT.template, self.DT)
        self.find_point_by_template(img_full, self.En.template, self.En)
        self.find_point_by_template(img_full, self.Go.template, self.Go)
        self.find_point_by_template(img_full, self.Me.template, self.Me)
        self.find_point_by_template(img_full, self.Mn.template, self.Mn)
        self.find_point_by_template(img_full, self.N.template, self.N)
        self.find_point_by_template(img_full, self.O.template, self.O)
        self.find_point_by_template(img_full, self.PAC.template, self.PAC)
        self.find_point_by_template(img_full, self.Pg.template, self.Pg)
        self.find_point_by_template(img_full, self.PNS.template, self.PNS)
        self.find_point_by_template(img_full, self.Pr.template, self.Pr)

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
                sum = thread_culc.calc_sum(x, y, resized_img, template, half_size_template)
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

        arr_sum_full = thread_culc.start(x_point_th, y_point_th, _img_full, _template_full, self.setting.threadNums,
                                         self.setting.processingSize)
        print("Потоки завершены")

        max_array_sum = 0
        for x in range(x_point_full - self.setting.processingSizeHalf, x_point_full + self.setting.processingSizeHalf):
            for y in range(y_point_full - self.setting.processingSizeHalf, y_point_full + self.setting.processingSizeHalf):
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
        for x in range(_x_point_full - self.setting.processingSizeHalf, _x_point_full + self.setting.processingSizeHalf):
            for y in range(_y_point_full - self.setting.processingSizeHalf, _y_point_full + self.setting.processingSizeHalf):
                color = int(((_arr_sum_full[
                    x - _x_point_full + self.setting.processingSizeHalf, y - _y_point_full + self.setting.processingSizeHalf]) / max_int) * 255)
                _img_full.putpixel((x, y), color)
        _img_full.show()

    def find_cephalometric_parameters(self):
        return 1
