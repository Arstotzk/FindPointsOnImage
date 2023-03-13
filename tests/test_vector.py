import unittest
from vector import Vec2
from point import Point
from PIL import Image


class TestVector(unittest.TestCase):

    def setUp(self):
        point1 = Point("point1", Image.open("img/N.png").convert('L'))
        point1.set_xy(2, 1)
        point2 = Point("point2", Image.open("img/N.png").convert('L'))
        point2.set_xy(1, 4)
        point3 = Point("point3", Image.open("img/N.png").convert('L'))
        point3.set_xy(4, 4)
        self.vector1 = Vec2(point1, point2, "vector1")
        self.vector2 = Vec2(point3, point2, "vector2")

    def test_angleBetweenRadians(self):
        self.assertEqual(round(self.vector1.angle_between_radians(self.vector2), 3), 1.249)

    def test_angleBetweenDegrees(self):
        self.assertEqual(round(self.vector1.angle_between_degrees(self.vector2), 3), 71.565)


if __name__ == "__main__":
    unittest.main()
