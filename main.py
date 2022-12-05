import numpy as np
from PIL import Image
from numpy import save
import time
from numpy import load
np.set_printoptions(threshold=np.inf)

def culcSum(_x, _y, _img, _shab):
    summ = 0
    xs = -1
    ys = -1
    for x in range (_x - 64, _x + 64):
        xs += 1
        ys = -1
        for y in range (_y - 64, _y + 64):
            ys += 1
            r = _img.getpixel((x, y))
            rs = _shab.getpixel((xs, ys))
            if (r == rs):
                summ += 1
            else:
                summ += 1/((r - rs) ** 2)
    return summ

startTime = int(round(time.time()*1000))
img = Image.open("img/1.jpg")
img = img.convert('L')
imgSum = Image.open("img/1.jpg")
imgSum = imgSum.convert('L')
shab = Image.open("img/1S.png")
shab = shab.convert('L')
width, height = img.size
arrSumm = np.full((width, height), 0)
save('arrZero.npy', arrSumm)
summOld = 0
for x in range (64, width-64):
    for y in range (64, height-64):
        summ = culcSum(x, y, img, shab)
        arrSumm[x, y] = summ
        if (summ > summOld):
            xPoint = x
            yPoint = y
    print("Ready: " + str(((x - 63)/(width-128)) * 100) + "%")
save('arrSumm2.npy', arrSumm)
maxArrSum = 0
for x in range (64, width-64):
    for y in range (64, height-64):
        nextArrSum = arrSumm[x, y]
        if (nextArrSum > maxArrSum):
            maxArrSum = nextArrSum
for x in range (64, width-64):
    for y in range (64, height-64):
        arrSumm[x, y] = int(((arrSumm[x, y])/maxArrSum) * 255)
for x in range (64, width-64):
    for y in range (64, height-64):
        imgSum.putpixel((x, y)(arrSumm[x, y], arrSumm[x, y], arrSumm[x, y]))
print(xPoint, yPoint)
#imgSum.show()
img.putpixel((xPoint,yPoint)(0, 255, 0))
#img.show()
endTime = int(round(time.time() * 1000))
difTime = endTime - startTime
print("Executing time: " + str(difTime))