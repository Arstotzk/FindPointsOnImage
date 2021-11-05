import numpy as np
from PIL import Image
from numpy import save
from numpy import load
import threading
from threading import Thread
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

def culcSumThread(_x, _y, _img, _shab, _size, _xStart):

    arrSumm = np.full((2, 32), 0)
    for x in range(_xStart, _xStart + 2):
        for y in range(0, 32):
            arrSumm[x,y] = culcSum(_x, _y, _img, _shab, _size)
    return arrSumm

def resizeImg(_img):
    width, height = _img.size
    new_width = int(width/8)
    new_height = int(height/8)
    print(new_width, new_height)
    _img = _img.resize((new_width, new_height), Image.ANTIALIAS)
    return _img

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
img = resizeImg(img)
imgSum = Image.open("img/1prepare.jpg")
imgSum = imgSum.convert('L')
imgSum = resizeImg(imgSum)
shab = Image.open("img/1S.png")
shab = shab.convert('L')
shab = resizeImg(shab)
width, height = img.size
arrSumm = np.full((width, height), 0)
#save('arrZero.npy', arrSumm)
summOld = 0
for x in range (8, width-8):
    for y in range (8, height-8):
        summ = culcSum(x, y, img, shab, 8)
        arrSumm[x, y] = summ
        if (summ > summOld):
            summOld = summ
            xPoint = x
            yPoint = y
    print("Ready resize: " + str(((x - 7)/(width-16)) * 100) + "%")
#save('arrSummMini.npy', arrSumm)
maxArrSum = 0
for x in range (8, width-8):
    for y in range (8, height-8):
        nextArrSum = arrSumm[x, y]
        if (nextArrSum > maxArrSum):
            maxArrSum = nextArrSum
for x in range (8, width-8):
    for y in range (8, height-8):
        arrSumm[x, y] = int(((arrSumm[x, y])/maxArrSum) * 255)
for x in range (8, width-8):
    for y in range (8, height-8):
        collor = int(arrSumm[x, y].item())
        imgSum.putpixel((x, y),(collor))
print(xPoint, yPoint)
#imgSum.show()
xPointFull = xPoint * 8
yPointFull = yPoint * 8
summOld = 0

for x in range (xPointFull-16, xPointFull+16):
    for y in range (yPointFull-16, yPointFull+16):
        summ = culcSum(x, y, imgFull, shabFull, 64)
        arrSummFull[x, y] = summ
        if (summ > summOld):
            summOld = summ
            xPoint = x
            yPoint = y
    print("Ready resize: " + str(((x - xPointFull + 16)/(32)) * 100) + "%")
maxArrSum = 0

width, height = imgShow.size
for x in range (xPointFull-16, xPointFull+16):
    for y in range (yPointFull-16, yPointFull+16):
        nextArrSum = arrSummFull[x, y]
        if (nextArrSum > maxArrSum):
            maxArrSum = nextArrSum
for x in range (xPointFull-16, xPointFull+16):
    for y in range (yPointFull-16, yPointFull+16):
        arrSummFull[x, y] = int(((arrSummFull[x, y])/maxArrSum) * 255)
for x in range (xPointFull-16, xPointFull+16):
    for y in range (yPointFull-16, yPointFull+16):
        collor = int(arrSummFull[x, y].item())
        imgSumFull.putpixel((x, y),(collor))
imgSumFull.show()
imgShow.putpixel((xPoint,yPoint),(0, 255, 0))
imgShow.show()