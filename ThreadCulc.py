import numpy as np
from concurrent.futures import ProcessPoolExecutor
import math

def culcSum(_x, _y, _img, _shab, _size):
    summ = 0
    xs = -1
    ys = -1
    width, height = _img.size
    for x in range (_x - _size, _x + _size):
        xs += 1
        ys = -1
        for y in range (_y - _size, _y + _size):
            ys += 1
            if width < x or height < y:
               continue
            r = _img.getpixel((x, y))
            rs = _shab.getpixel((xs, ys))
            if (r == rs):
                summ += 1
            else:
                summ += 1/((r - rs) ** 2)
    return summ

def culcSumThread(_x, _y, _img, _shab, _size, i, blocks, processingSize):
    arrSumm = None
    for block in blocks:
        if blocks[0] == block:
            arrSumm = culcSumBlock(_x, _y, _img, _shab, _size, block, processingSize)
        else:
            arrSummBlock = culcSumBlock(_x, _y, _img, _shab, _size, block, processingSize)
            arrSumm = np.vstack((arrSumm, arrSummBlock))
    print("Поток " + str(i) + " завершен")
    return arrSumm

def culcSumBlock(_x, _y, _img, _shab, _size, block, processingSize):
    _xStart = (block * 2) - 2
    arrSumm = np.full((2, processingSize), 0)
    for x in range(_xStart, _xStart + 2):
        for y in range(0, processingSize):
            arrSumm[x - _xStart, y] = culcSum(_x + x, _y + y, _img, _shab, _size)
    print("Расчет блока " + str(block) + " завершен")
    return arrSumm

#Получить блоки для расчета на поток
def getBlocksByThreads(threadNum, threadNums, processingSize):
    blocksNum = int(processingSize/2)
    blocks = []
    maxBlockNum = math.ceil(processingSize/threadNums)
    for iteration in range(0, maxBlockNum - 1):
        blockNum = int(threadNum + threadNums * iteration)
        if (blockNum < blocksNum):
            blocks.append(blockNum)
    return blocks

def start (xPointTh,yPointTh, imgFull,shabFull, threadNums, processingSize):
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
    return result