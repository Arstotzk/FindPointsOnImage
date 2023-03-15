import unittest
from PIL import Image
from normalization import Normalization


class TestNormalization(unittest.TestCase):

    def setUp(self):
        self.img1 = Image.open("img/1prepare2.jpg")
        self.img2 = Image.open("img/2prepare.jpg")

    def test_normalization_image_1(self):
        norm = Normalization(self.img1)
        norm.normalize()
        norm.show_img_normalize()

    def test_normalization_image_2(self):
        norm = Normalization(self.img2)
        norm.normalize()
        norm.show_img_normalize()


if __name__ == '__main__':
    unittest.main()
