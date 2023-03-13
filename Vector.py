import math
import Point
import numpy as np


class Vec2:

    def __init__(self, _pointStart, _pointEnd, _name):
        self.X = _pointEnd.X - _pointStart.X
        self.Y = _pointEnd.Y - _pointStart.Y
        self.array = [self.X, self.Y]
        self.name = _name

    def unitVector(self):
        return self.array / np.linalg.norm(self.array)

    def angleBetweenRadians(self, vector2):
        v1_u = self.unitVector()
        v2_u = vector2.unitVector()
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def angleBetweenDegrees(self, vector2):
        radians = self.angleBetweenRadians(vector2)
        return np.degrees([radians.real])[0]
