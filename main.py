import numpy as np
from PIL import Image

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


img = Image.open("img/1.jpg")
#img = img.convert('1')
img = img.convert('L')
shab = Image.open("img/1S.png")
shab = shab.convert('L')
width, height = img.size
summOld = 0
for x in range (64, width-64):
    for y in range (64, height-64):
        summ = culcSum(x,y,img,shab)
        if (summ > summOld):
            xPoint = x
            yPoint = y
    print("Ready: " + str(((x - 63)/(width-128)) * 100) + "%")
print(xPoint, yPoint)
img.putpixel((xPoint,yPoint)(0, 255, 0))
img.show()