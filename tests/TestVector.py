import unittest
from Vector import Vec2
from Point import Point
from PIL import Image

class TestCalculator(unittest.TestCase):

  def setUp(self):
    point1 = Point("point1", Image.open("img/N.png").convert('L'))
    point1.X = 2
    point1.Y = 1
    point2 = Point("point2", Image.open("img/N.png").convert('L'))
    point2.X = 1
    point2.Y = 4
    point3 = Point("point3", Image.open("img/N.png").convert('L'))
    point3.X = 4
    point3.Y = 4
    self.vector1 = Vec2(point1, point2, "vector1")
    self.vector2 = Vec2(point3, point2, "vector2")

  def test_angleBetweenRadians(self):
    self.assertEqual(round(self.vector1.angleBetweenRadians(self.vector2), 3), 1.249)

  def test_angleBetweenDegrees(self):
    self.assertEqual(round(self.vector1.angleBetweenDegrees(self.vector2), 3), 71.565)

if __name__ == "__main__":
  unittest.main()