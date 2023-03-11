import numpy as np
from PIL import Image
import time
import ThreadCulc
import Point
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
        self.resizedImage = self.resizeImg(self.image, self.setting.multipleResize)
        self.width, self.height = self.image.size
        self.arrSummFull = np.full((self.width, self.height), 0)
        #Точки
        self.A = Point.Point("A", Image.open("img/A.png").convert('L'))
        self.A1 = Point.Point("A1", Image.open("img/A1.png").convert('L'))
        self.ANS = Point.Point("ANS", Image.open("img/ANS.png").convert('L'))
        self.AR = Point.Point("AR", Image.open("img/AR.png").convert('L'))
        self.B = Point.Point("B", Image.open("img/B.png").convert('L'))
        self.B1 = Point.Point("B1", Image.open("img/B1.png").convert('L'))
        self.BR = Point.Point("BR", Image.open("img/BR.png").convert('L'))
        self.DT = Point.Point("DT", Image.open("img/DT.png").convert('L'))
        self.En = Point.Point("En", Image.open("img/En.png").convert('L'))
        self.Go = Point.Point("Go", Image.open("img/Go.png").convert('L'))
        self.Me = Point.Point("Me", Image.open("img/Me.png").convert('L'))
        self.Mn = Point.Point("Mn", Image.open("img/Mn.png").convert('L'))
        self.N = Point.Point("N", Image.open("img/N.png").convert('L'))
        self.O = Point.Point("O", Image.open("img/O.png").convert('L'))
        self.PAC = Point.Point("PAC", Image.open("img/PAC.png").convert('L'))
        self.Pg = Point.Point("Pg", Image.open("img/Pg.png").convert('L'))
        self.PNS = Point.Point("PNS", Image.open("img/PNS.png").convert('L'))
        self.Pr = Point.Point("Pr", Image.open("img/Pr.png").convert('L'))

    def executionTime(self):
        """
        Возвращает время затраченое на обработку изображения.
        :return: Время в мс.
        """
        return self.endTime - self.startTime

    def setPointsOnImege(self):
        """
        Ставит на изображение найденные точки.
        """
        self.A.setPointOnImage(self.image)
        self.A1.setPointOnImage(self.image)
        self.ANS.setPointOnImage(self.image)
        self.AR.setPointOnImage(self.image)
        self.B.setPointOnImage(self.image)
        self.B1.setPointOnImage(self.image)
        self.BR.setPointOnImage(self.image)
        self.DT.setPointOnImage(self.image)
        self.En.setPointOnImage(self.image)
        self.Go.setPointOnImage(self.image)
        self.Me.setPointOnImage(self.image)
        self.Mn.setPointOnImage(self.image)
        self.N.setPointOnImage(self.image)
        self.O.setPointOnImage(self.image)
        self.PAC.setPointOnImage(self.image)
        self.Pg.setPointOnImage(self.image)
        self.PNS.setPointOnImage(self.image)
        self.Pr.setPointOnImage(self.image)

    def resizeImg(self, _img, multiple):
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

    def findPointsByTemplate(self):
        """
        Найти точки по шаблону.
        """
        self.startTime = int(round(time.time() * 1000))
        imgFull = self.image
        imgFull = imgFull.convert('L')

        self.findPointByTemplate(imgFull, self.A.template, self.A)
        self.findPointByTemplate(imgFull, self.A1.template, self.A1)
        self.findPointByTemplate(imgFull, self.ANS.template, self.ANS)
        self.findPointByTemplate(imgFull, self.AR.template, self.AR)
        self.findPointByTemplate(imgFull, self.B.template, self.B)
        self.findPointByTemplate(imgFull, self.B1.template, self.B1)
        self.findPointByTemplate(imgFull, self.BR.template, self.BR)
        self.findPointByTemplate(imgFull, self.DT.template, self.DT)
        self.findPointByTemplate(imgFull, self.En.template, self.En)
        self.findPointByTemplate(imgFull, self.Go.template, self.Go)
        self.findPointByTemplate(imgFull, self.Me.template, self.Me)
        self.findPointByTemplate(imgFull, self.Mn.template, self.Mn)
        self.findPointByTemplate(imgFull, self.N.template, self.N)
        self.findPointByTemplate(imgFull, self.O.template, self.O)
        self.findPointByTemplate(imgFull, self.PAC.template, self.PAC)
        self.findPointByTemplate(imgFull, self.Pg.template, self.Pg)
        self.findPointByTemplate(imgFull, self.PNS.template, self.PNS)
        self.findPointByTemplate(imgFull, self.Pr.template, self.Pr)

        self.endTime = int(round(time.time() * 1000))

    def findPointByTemplate(self, _imgFull, _shabFull, _point):
        """
        Нахождение точки по шаблону.
        :param _imgFull: Изображение.
        :param _shabFull: Шаблон.
        :param _point: Точка.
        """
        resizedImg = self.resizedImage
        resizedImg = resizedImg.convert('L')
        shab = _shabFull
        shab = shab.convert('L')
        shab = self.resizeImg(shab, self.setting.multipleResize)
        width, height = resizedImg.size
        widthShab, heightShab = shab.size
        halfSizeShab = int(widthShab / 2)
        arrSumm = np.full((width, height), 0)

        summOld = 0
        for x in range(halfSizeShab, width - (halfSizeShab)):
            for y in range(halfSizeShab, height - (halfSizeShab)):
                summ = ThreadCulc.culcSum(x, y, resizedImg, shab, halfSizeShab)
                arrSumm[x, y] = summ
                if (summ > summOld):
                    summOld = summ
                    xPoint = x
                    yPoint = y
            # print("Ready resize: " + str(((x - halfSizeShab + 1) / (width - widthShab)) * 100) + "%")

        print(xPoint, yPoint)

        xPointFull = xPoint * self.setting.multipleResize
        yPointFull = yPoint * self.setting.multipleResize
        print(xPointFull, yPointFull)

        xPointTh = xPointFull - self.setting.processingSizeHalf
        yPointTh = yPointFull - self.setting.processingSizeHalf

        numsss = ThreadCulc.start(xPointTh, yPointTh, _imgFull, _shabFull, self.setting.threadNums, self.setting.processingSize)
        print("Потоки завершены")

        arrSummFull = numsss[0]
        for i in range(1, self.setting.threadNums):
            arrSummFull = np.vstack((arrSummFull, numsss[i]))

        maxArrSum = 0
        for x in range(xPointFull - self.setting.processingSizeHalf, xPointFull + self.setting.processingSizeHalf):
            for y in range(yPointFull - self.setting.processingSizeHalf, yPointFull + self.setting.processingSizeHalf):
                nextArrSum = arrSummFull[x - xPointFull + self.setting.processingSizeHalf, y - yPointFull + self.setting.processingSizeHalf]
                if (nextArrSum > maxArrSum):
                    maxArrSum = nextArrSum
                    _point.X = x
                    _point.Y = y


        #Отображение градиента нахождения точки
        #maxInt = arrSummFull.max()
        #for x in range(xPointFull - templateConst, xPointFull + templateConst):
        #    for y in range(yPointFull - templateConst, yPointFull + templateConst):
        #        collor = int(((arrSummFull[x - xPointFull + templateConst, y - yPointFull + templateConst])/maxInt) * 255)
        #        _imgFull.putpixel((x, y),(collor))
        #_imgFull.show()