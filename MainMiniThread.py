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
import configRead
import ImageOperations

if __name__ == '__main__':
    image = Image.open("img/1prepare.jpg")
    imageOper = ImageOperations.ImageOperations(image, configRead.Settings())
    imageOper.findPointsByTemplate()
    print("Executing time: " + str(imageOper.executionTime()))
    imageOper.getPointOnImage()
    imageOper.imageFirstPoint.show()
