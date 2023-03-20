from PIL import Image, ImageFilter
import cv2
import numpy as np
from config_read import Settings

def resize_img(_img, multiple):
    """
    Уменьшение изображение.
    :param _img: Исходное изображение.
    :param multiple: Коэффициент уменьшения.
    :return:
    """
    width, height = _img.size
    new_width = int(width / multiple)
    new_height = int(height / multiple)
    _img = _img.resize((new_width, new_height), Image.ANTIALIAS)
    return _img

class Normalization:
    def __init__(self, _img):
        self.img = _img
        self.imgNormalize = _img.copy()
        self.imgCv = None
        self.kernel = np.ones((5, 5), np.uint8)
        self.normalizeSize = Settings().skullNormalizationSize

    def normalize(self):
        imgEdges = self.img.copy().convert("L")
        imgEdges = imgEdges.filter(ImageFilter.FIND_EDGES).convert("RGB")
        self.imgCv = cv2.cvtColor(np.array(imgEdges), cv2.COLOR_RGB2GRAY)

        average_color_row = np.average(self.imgCv, axis=0)
        average_color = np.average(average_color_row, axis=0)

        (thresh, self.imgCv) = cv2.threshold(self.imgCv, int(average_color * 2), 255, cv2.THRESH_BINARY)

        self.imgCv = cv2.dilate(self.imgCv, self.kernel, iterations=1)
        self.imgCv = cv2.erode(self.imgCv, self.kernel, iterations=2)
        self.imgCv = cv2.dilate(self.imgCv, self.kernel, iterations=1)

        contours, hierarchy = cv2.findContours(self.imgCv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.imgCv = cv2.cvtColor(np.array(self.imgCv), cv2.COLOR_GRAY2RGB)
        if len(contours) != 0:
            max_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_contour)

        resizing = w / self.normalizeSize
        self.imgNormalize = resize_img(self.imgNormalize, resizing)

    def show_img_normalize(self):
        self.imgNormalize.show()