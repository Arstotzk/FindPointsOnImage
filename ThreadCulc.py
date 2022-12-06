import numpy as np
from concurrent.futures import ProcessPoolExecutor

def culcSum(_x, _y, _img, _shab, _size):
    summ = 0
    xs = -1
    ys = -1
    for x in range (_x - _size, _x + _size):
        xs += 1
        ys = -1
        for y in range (_y - _size, _y + _size):
            ys += 1
            r = _img.getpixel((x, y))
            rs = _shab.getpixel((xs, ys))
            if (r == rs):
                summ += 1
            else:
                summ += 1/((r - rs) ** 2)
    return summ

def culcSumThread(_x, _y, _img, _shab, _size, i, blocks):
    arrSumm = None
    for block in blocks:
        if blocks[0] == block:
            arrSumm = culcSumBlock(_x, _y, _img, _shab, _size, block)
        else:
            arrSummBlock = culcSumBlock(_x, _y, _img, _shab, _size, block)
            arrSumm = np.vstack((arrSumm, arrSummBlock))
    print("Поток " + str(i) + " завершен")
    return arrSumm

def culcSumBlock(_x, _y, _img, _shab, _size, block):
    _xStart = (block * 2) - 2
    arrSumm = np.full((2, 32), 0)
    for x in range(_xStart, _xStart + 2):
        for y in range(0, 32):
            arrSumm[x - _xStart, y] = culcSum(_x + x, _y + y, _img, _shab, _size)
    print("Расчет блока " + str(block) + " завершен")
    return arrSumm

#Получить блоки для расчета на поток
def getBlocksByThreads(threadNum, threadNums, threadsCPU):
    blocksNum = int(threadsCPU/threadNums)
    blocks = []
    for block in range(0, blocksNum):
        blocks.append(int((threadNum * blocksNum) + block))
    return blocks

def start (xPointTh,yPointTh, imgFull,shabFull, threadNums, threadsCPU):
    executor = ProcessPoolExecutor(threadNums)
    params = [[],[],[],[],[],[],[]]
    for threadNum in range(0, threadNums):
        params[0].append(xPointTh)
        params[1].append(yPointTh)
        params[2].append(imgFull)
        params[3].append(shabFull)
        params[4].append(64)
        params[5].append(threadNum)
        params[6].append(getBlocksByThreads(threadNum, threadNums, threadsCPU))

    result = list(executor.map(culcSumThread, *params))
    return result