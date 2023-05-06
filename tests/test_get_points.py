import unittest

from db_connect import DBConnect
from point import Points


class TestGetPoints(unittest.TestCase):

    def setUp(self):
        self.connect = DBConnect()
        self.image_guid = "df19465c-9b91-426e-9130-7c2ebfad0607"

    def test_GetCephalometricPoints(self):

        result = self.connect.ExecuteQuery('SELECT x, y, point_type FROM public.points where image = \'' + self.image_guid + '\';')
        print(result)
        self.points = Points()
        for pointData in result:
            point = self.points.GetPointByTypeGuid(pointData[2])
            print("point guid: " + pointData[2])
            print("point name: " + point.name)
            print("x: " + pointData[0].__str__())
            print("y: " + pointData[1].__str__())

        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
