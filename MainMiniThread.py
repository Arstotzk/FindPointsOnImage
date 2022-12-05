import concurrent

import numpy as np
from PIL import Image
import time
from numpy import save
from numpy import load
import threading
from threading import Thread
import os
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor
import ThreadCulc

np.set_printoptions(threshold=np.inf)

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

def culcSumThread(_x, _y, _img, _shab, _size, i):
    _xStart = (i * 2) - 2
    arrSumm = np.full((2, 32), 0)
    for x in range(_xStart, _xStart + 2):
        for y in range(0, 32):
            arrSumm[x - _xStart, y] = culcSum(_x + x, _y + y, _img, _shab, _size)
    print("Поток " + str(i) + " завершен")
    #return arrSumm

def resizeImg(_img, multiple):
    width, height = _img.size
    new_width = int(width/multiple)
    new_height = int(height/multiple)
    #print(new_width, new_height)
    _img = _img.resize((new_width, new_height), Image.ANTIALIAS)
    return _img

threadsCPU = 16
threadNums = 1
multipleResize = 8
startTime = int(round(time.time()*1000))
imgShow = Image.open("img/1prepare.jpg")
imgFull = Image.open("img/1prepare.jpg")
imgFull = imgFull.convert('L')
imgSumFull = Image.open("img/1prepare.jpg")
imgSumFull = imgSumFull.convert('L')
shabFull = Image.open("img/1S.png")
shabFull = shabFull.convert('L')
width, height = imgShow.size
arrSummFull = np.full((width, height), 0)

img = Image.open("img/1prepare.jpg")
img = img.convert('L')
img = resizeImg(img, multipleResize)
imgSum = Image.open("img/1prepare.jpg")
imgSum = imgSum.convert('L')
imgSum = resizeImg(imgSum, multipleResize)
shab = Image.open("img/1S.png")
shab = shab.convert('L')
shab = resizeImg(shab, multipleResize)
width, height = img.size
widthShab, heightShab = shab.size
halfSizeShab = int(widthShab/2)
arrSumm = np.full((width, height), 0)
#save('arrZero.npy', arrSumm)
summOld = 0
for x in range (halfSizeShab, width-(halfSizeShab)):
    for y in range (halfSizeShab, height-(halfSizeShab)):
        summ = culcSum(x, y, img, shab, halfSizeShab)
        arrSumm[x, y] = summ
        if (summ > summOld):
            summOld = summ
            xPoint = x
            yPoint = y
    if __name__ == '__main__':
        print("Ready resize: " + str(((x - halfSizeShab + 1)/(width - widthShab)) * 100) + "%")
#save('arrSummMini.npy', arrSumm)

#maxArrSum = 0
#for x in range (halfSizeShab, width-halfSizeShab):
#    for y in range (halfSizeShab, height-halfSizeShab):
#        nextArrSum = arrSumm[x, y]
#        if (nextArrSum > maxArrSum):
#            maxArrSum = nextArrSum
#for x in range (halfSizeShab, width-halfSizeShab):
#    for y in range (halfSizeShab, height-halfSizeShab):
#        arrSumm[x, y] = int(((arrSumm[x, y])/maxArrSum) * 255)
#for x in range (halfSizeShab, width-halfSizeShab):
#    for y in range (halfSizeShab, height-halfSizeShab):
#        collor = int(arrSumm[x, y].item())
#        imgSum.putpixel((x, y),(collor))

if __name__ == '__main__':
    print(xPoint, yPoint)
#imgSum.show()
xPointFull = xPoint * 8
yPointFull = yPoint * 8
summOld = 0

xPointTh = xPointFull-16
yPointTh = yPointFull-16

if __name__ == '__main__':
    numsss = ThreadCulc.start(xPointTh, yPointTh, imgFull, shabFull, threadNums, threadsCPU)
    print("Потоки завершены")
    #print(numsss)
    #Закоментил на время эксперемента
    arrSummFull = numsss[0]
    for i in range(1,threadNums):
        arrSummFull = np.vstack((arrSummFull, numsss[i]))
    #arrSummFull = np.vstack((numsss[0], numsss[1], numsss[2], numsss[3], numsss[4], numsss[5], numsss[6], numsss[7], numsss[8], numsss[9], numsss[10], numsss[11], numsss[12], numsss[13], numsss[14], numsss[15]))
    #print(arrSummFull)
    #for x in range (xPointFull-16, xPointFull+16):
    #    for y in range (yPointFull-16, yPointFull+16):
    #        summ = culcSum(x, y, imgFull, shabFull, 64)
    #        arrSummFull[x, y] = summ
    #        if (summ > summOld):
    #            summOld = summ
    #            xPoint = x
    #            yPoint = y
    #    print("Ready: " + str(((x - xPointFull + 16)/(32)) * 100) + "%")
    maxArrSum = 0

    #Закоментил на время эксперемента
    for x in range (xPointFull-16, xPointFull+16):
        for y in range (yPointFull-16, yPointFull+16):
            nextArrSum = arrSummFull[x - xPointFull + 16, y - yPointFull + 16]
            if (nextArrSum > maxArrSum):
                maxArrSum = nextArrSum
    for x in range (xPointFull-16, xPointFull+16):
        for y in range (yPointFull-16, yPointFull+16):
            arrSummFull[x - xPointFull + 16, y - yPointFull + 16] = int(((arrSummFull[x - xPointFull + 16, y - yPointFull + 16])/maxArrSum) * 255)
    for x in range (xPointFull-16, xPointFull+16):
        for y in range (yPointFull-16, yPointFull+16):
            collor = int(arrSummFull[x - xPointFull + 16, y - yPointFull + 16].item())
            imgSumFull.putpixel((x, y),(collor))

    endTime = int(round(time.time() * 1000))
    difTime = endTime - startTime
    print("Executing time: " + str(difTime))
    imgSumFull.show()
    #imgShow.putpixel((xPoint,yPoint),(0, 255, 0))
    #imgShow.show()