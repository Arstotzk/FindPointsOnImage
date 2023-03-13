import numpy as np
from concurrent.futures import ProcessPoolExecutor
import math

class ArrSumm:

    def __init__(self):
        self.arrays = []
        self.blocks = []

def culcSum(_x, _y, _img, _shab, _size):
    """
    Рачет суммы совпадения пикселя и области вокруг него с шаблоном.
    :param _x: X координата пикселя.
    :param _y: Y координата пикселя.
    :param _img: Изображение.
    :param _shab: Шаблон.
    :param _size: Размер шаблона\2.
    :return: Сумма сопадения пикселя с шаблоном.
    """
    summ = 0
    xs = -1
    ys = -1
    width, height = _img.size
    for x in range(_x - _size, _x + _size):
        xs += 1
        ys = -1
        for y in range(_y - _size, _y + _size):
            ys += 1
            if width <= x or height <= y:
               continue
            r = _img.getpixel((x, y))
            rs = _shab.getpixel((xs, ys))
            if (r == rs):
                summ += 1
            else:
                summ += 1/((r - rs) ** 2)
    return summ

def culcSumThread(_x, _y, _img, _shab, _size, thread, blocks, processingSize):
    """
    Расчет совпадения шаблона через потоки.
    :param _x: X координата начала области для обработки.
    :param _y: Y координата начала области для обработки.
    :param _img: Изображение.
    :param _shab: Шаблон.
    :param _size: Размер шаблона\2.
    :param i: Номер потока.
    :param blocks: Блоки для обработки.
    :param processingSize: Область для обработки.
    :return: Массив совпадений по найденным блокам в потоке.
    """
    arrSumm = ArrSumm()
    for block in blocks:
        arrSumm.arrays.append(culcSumBlock(_x, _y, _img, _shab, _size, block, processingSize))
        arrSumm.blocks.append(block)

    print("Поток " + str(thread) + " завершен")
    return arrSumm

def culcSumBlock(_x, _y, _img, _shab, _size, block, processingSize):
    """
    Расчет суммы совпадения на область в блоке.
    :param _x: X координата начала области для обработки.
    :param _y: Y координата начала области для обработки.
    :param _img: Изображение.
    :param _shab: Шаблон.
    :param _size: Размер шаблона\2.
    :param block: Номер блока.
    :param processingSize: Область обработки.
    :return: Сумма совпадений по блоку.
    """
    _xStart = (block * 2) - 2
    arrSumm = np.full((2, processingSize), 0)
    for x in range(_xStart, _xStart + 2):
        for y in range(0, processingSize):
            arrSumm[x - _xStart, y] = culcSum(_x + x, _y + y, _img, _shab, _size)
    print("Расчет блока " + str(block) + " завершен")
    return arrSumm

def getBlocksByThreads(threadNum, threadNums, processingSize):
    """
    Получить блоки для расчета на поток.
    Делит область на блоки по 2 пикселя шириной, затем по потоку назначает блоки в цикле.
    Соответствие потока и блока вычисляется: номер блока = (номер потока + всего потоков * x),
    где x - номер итерации по прохождению массива блоков.
    :param threadNum: Номер потока.
    :param threadNums: Всего потоков.
    :param processingSize: Размер области обработки.
    :return: Массив блоков соответствующий номеру потока.
    """
    blocksNum = int(processingSize/2)
    blocks = []
    maxBlockNum = math.ceil(processingSize/threadNums)
    for iteration in range(0, maxBlockNum - 1):
        blockNum = int(threadNum + threadNums * iteration)
        if (blockNum < blocksNum):
            blocks.append(blockNum)
    return blocks

def start (xPointTh,yPointTh, imgFull,shabFull, threadNums, processingSize):
    """
    Старт расчета через многопоточный процесс.
    :param xPointTh: X координата начала области для обработки.
    :param yPointTh: Y координата начала области для обработки.
    :param imgFull: Изображение.
    :param shabFull: Шаблон.
    :param threadNums: Кол-во потоков.
    :param processingSize: Размер области обработки.
    :return: Массив с вероятностным нахождением точки по пикселям области.
    """
    executor = ProcessPoolExecutor(threadNums)
    params = [[],[],[],[],[],[],[],[]]
    for threadNum in range(0, threadNums):
        params[0].append(xPointTh)
        params[1].append(yPointTh)
        params[2].append(imgFull)
        params[3].append(shabFull)
        params[4].append(int(shabFull.size[0]/2))
        params[5].append(threadNum)
        params[6].append(getBlocksByThreads(threadNum, threadNums, processingSize))
        params[7].append(processingSize)

    result = list(executor.map(culcSumThread, *params))

    #Собираем массивы блоков в один двумерный массив
    blockCounter = 0
    blockEnd = int(processingSize/2)
    resultArray = None
    while blockCounter < blockEnd:
        for arrSumm in result:
            counter = 0
            for blockNum in arrSumm.blocks:
                if blockNum == blockCounter and blockNum == 0:
                    resultArray = arrSumm.arrays[counter][0]
                    resultArray = np.vstack((resultArray, arrSumm.arrays[counter][1]))
                    blockCounter = blockCounter + 1
                elif blockNum == blockCounter:
                    resultArray = np.vstack((resultArray, arrSumm.arrays[counter][0]))
                    resultArray = np.vstack((resultArray, arrSumm.arrays[counter][1]))
                    blockCounter = blockCounter + 1
                counter = counter + 1

    return resultArray