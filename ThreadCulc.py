import concurrent

import numpy as np
from PIL import Image
from numpy import save
from numpy import load
import threading
from threading import Thread
import os
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

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
    #params = [
    #    [xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh],
    #    [yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh],
    #    [imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull],
    #    [shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull],
    #    [64,64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64],
    #    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
    #    [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15]]
    #]
    #executor = ProcessPoolExecutor(8)
    #params = [
    #    [xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh, xPointTh],
    #    [yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh, yPointTh],
    #    [imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull, imgFull],
    #    [shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull, shabFull],
    #    [64, 64, 64, 64, 64, 64, 64, 64],
    #    [0, 1, 2, 3, 4, 5, 6, 7]
    #]
    result = list(executor.map(culcSumThread, *params))
    ##procs = []
    #    th = []
    #    pool = ProcessPoolExecutor(16)
    #    with concurrent.futures.ProcessPoolExecutor() as executor:

    #        for i in range(16):
    #            th.append(executor.map(culcSumThread, (xPointTh, yPointTh, imgFull, shabFull, 64, i, )))

    #    for x in as_completed(th):
    #        print(x.result())
    #for i in range(16):
    #    th = Process(target=culcSumThread, args=(xPointTh, yPointTh, imgFull, shabFull, 64, i, ))
    #    procs.append(th)
    #    th.start()

    #for proc in procs:
    #    proc.join()
    #print("Потоки завершены")
    return result