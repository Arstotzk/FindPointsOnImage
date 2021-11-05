import numpy as np
from PIL import Image
from numpy import save
from numpy import load
np.set_printoptions(threshold=np.inf)

def culcSum(_x, _y, _img, _shab):
    summ = 0
    xs = -1
    ys = -1
    for x in range (_x - 8, _x + 8):
        xs += 1
        ys = -1
        for y in range (_y - 8, _y + 8):
            ys += 1
            r = _img.getpixel((x, y))
            rs = _shab.getpixel((xs, ys))
            if (r == rs):
                summ += 1
            else:
                summ += 1/((r - rs) ** 2)
    return summ

def resizeImg(_img):
    width, height = _img.size
    new_width = int(width/8)
    new_height = int(height/8)
    print(new_width, new_height)
    _img = _img.resize((new_width, new_height), Image.ANTIALIAS)
    return _img

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
save('arrZero.npy', arrSumm)
summOld = 0
for x in range (8, width-8):
    for y in range (8, height-8):
        summ = culcSum(x, y, img, shab)
        arrSumm[x, y] = summ
        if (summ > summOld):
            xPoint = x
            yPoint = y
    print("Ready: " + str(((x - 7)/(width-16)) * 100) + "%")
save('arrSummMini.npy', arrSumm)
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
imgSum.show()
img.putpixel((xPoint,yPoint)(0, 255, 0))
img.show()