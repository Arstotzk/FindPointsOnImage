from numpy import load
import numpy as np
from PIL import Image
np.set_printoptions(threshold=np.inf)

imgSum = Image.open("img/1.jpg")
imgSum = imgSum.convert('L')
width, height = imgSum.size
maxArrSum = 0

arrSumm = np.load('arrSumm.npy')
for x in range(64, width - 64):
    for y in range(64, height - 64):
        nextArrSum = arrSumm[x, y]
        if (nextArrSum > maxArrSum):
            maxArrSum = nextArrSum
for x in range (64, width-64):
    for y in range (64, height-64):
        arrSumm[x, y] = int(((arrSumm[x, y])/maxArrSum) * 255)
print(arrSumm)
for x in range(64, width - 64):
    for y in range(64, height - 64):
        collor = int(arrSumm[x, y].item())
        imgSum.putpixel((x, y), (collor))
imgSum.show()
