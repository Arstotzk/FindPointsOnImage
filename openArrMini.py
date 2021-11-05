from numpy import load
import numpy as np
from PIL import Image
np.set_printoptions(threshold=np.inf)

imgSum = Image.open("img/1prepare.jpg")
imgSum = imgSum.convert('L')
width, height = imgSum.size
width = int(width/8)
height = int(height/8)
maxArrSum = 0
imgSum = imgSum.resize((width-16, height-16), Image.ANTIALIAS)



arrSumm = np.load('arrSummMini.npy')
for x in range(8, width - 8):
    for y in range(8, height - 8):
        nextArrSum = arrSumm[x, y]
        if (nextArrSum > maxArrSum):
            maxArrSum = nextArrSum
for x in range (8, width-8):
    for y in range (8, height-8):
        arrSumm[x, y] = int(((arrSumm[x, y])/maxArrSum) * 255)
#print(arrSumm)
for x in range(8, width-8):
    for y in range(8, height-8):
        collor = int(arrSumm[x, y].item())
        imgSum.putpixel((x-8, y-8), (collor))
imgSum.show()
