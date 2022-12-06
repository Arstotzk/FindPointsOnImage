import numpy as np
from PIL import Image
import time
import ThreadCulc
import configRead
np.set_printoptions(threshold=np.inf)

class ImageOperations:

    def __init__(self, _image, _setting):
        self.setting = _setting
        self.startTime = None
        self.endTime = None
        self.difTime = None
        self.image = _image
        self.resizedImage = self.resizeImg(self.image, self.setting.multipleResize)
        self.imageFirstPoint = None
        self.firstPointX = None
        self.firstPointY = None
        self.firstPointTemplate = Image.open("img/1S.png").convert('L')
        self.firstPointTemplateWidth, self.firstPointTemplateHeight = self.firstPointTemplate.size
        self.width, self.height = self.image.size
        self.arrSummFull = np.full((self.width, self.height), 0)
        self.coeficient = 2

    def executionTime(self):
        return self.endTime - self.startTime

    def resizeImg(self, _img, multiple):
        width, height = _img.size
        new_width = int(width / multiple)
        new_height = int(height / multiple)
        _img = _img.resize((new_width, new_height), Image.ANTIALIAS)
        return _img

    def culcSum(self, _x, _y, _img, _shab, _size):
        summ = 0
        xs = -1
        ys = -1
        for x in range(_x - _size, _x + _size):
            xs += 1
            ys = -1
            for y in range(_y - _size, _y + _size):
                ys += 1
                r = _img.getpixel((x, y))
                rs = _shab.getpixel((xs, ys))
                if (r == rs):
                    summ += 1
                else:
                    summ += 1 / ((r - rs) ** 2)
        return summ

    def findPointsByTemplate(self):
        self.startTime = int(round(time.time() * 1000))
        imgFull = self.image
        imgFull = imgFull.convert('L')
        shabFull = self.firstPointTemplate
        shabFull = shabFull.convert('L')

        resizedImg = self.resizedImage
        resizedImg = resizedImg.convert('L')
        shab = self.firstPointTemplate
        shab = shab.convert('L')
        shab = self.resizeImg(shab, self.setting.multipleResize)
        width, height = resizedImg.size
        widthShab, heightShab = shab.size
        halfSizeShab = int(widthShab / 2)
        arrSumm = np.full((width, height), 0)

        summOld = 0
        for x in range(halfSizeShab, width - (halfSizeShab)):
            for y in range(halfSizeShab, height - (halfSizeShab)):
                summ = self.culcSum(x, y, resizedImg, shab, halfSizeShab)
                arrSumm[x, y] = summ
                if (summ > summOld):
                    summOld = summ
                    xPoint = x
                    yPoint = y
            #print("Ready resize: " + str(((x - halfSizeShab + 1) / (width - widthShab)) * 100) + "%")

        print(xPoint, yPoint)

        xPointFull = xPoint * self.setting.multipleResize
        yPointFull = yPoint * self.setting.multipleResize
        summOld = 0

        xPointTh = xPointFull - 16
        yPointTh = yPointFull - 16

        numsss = ThreadCulc.start(xPointTh, yPointTh, imgFull, shabFull, self.setting.threadNums, self.setting.threadsCPU)
        print("Потоки завершены")

        arrSummFull = numsss[0]
        for i in range(1, self.setting.threadNums):
            arrSummFull = np.vstack((arrSummFull, numsss[i]))

        maxArrSum = 0
        for x in range(xPointFull - 16, xPointFull + 16):
            for y in range(yPointFull - 16, yPointFull + 16):
                nextArrSum = arrSummFull[x - xPointFull + 16, y - yPointFull + 16]
                if (nextArrSum > maxArrSum):
                    maxArrSum = nextArrSum
                    self.firstPointX = x
                    self.firstPointY = y

        #Градиент на изображении вероятности совпадения шаблона
        #for x in range(xPointFull - 16, xPointFull + 16):
        #    for y in range(yPointFull - 16, yPointFull + 16):
        #        arrSummFull[x - xPointFull + 16, y - yPointFull + 16] = int(
        #            ((arrSummFull[x - xPointFull + 16, y - yPointFull + 16]) / maxArrSum) * 255)
        #for x in range(xPointFull - 16, xPointFull + 16):
        #    for y in range(yPointFull - 16, yPointFull + 16):
        #        collor = int(arrSummFull[x - xPointFull + 16, y - yPointFull + 16].item())
        #        imgSumFull.putpixel((x, y), (collor))

        self.endTime = int(round(time.time() * 1000))

    def getPointOnImage(self):
        self.imageFirstPoint = self.image
        self.imageFirstPoint.putpixel((self.firstPointX, self.firstPointY), (0, 255, 0))