import math
import point
import numpy as np


class Vec2:

    def __init__(self, _point_start, _point_end, _name):
        self.X = _point_end.X - _point_start.X
        self.Y = _point_end.Y - _point_start.Y
        self.array = [self.X, self.Y]
        self.name = _name

    def unit_vector(self):
        return self.array / np.linalg.norm(self.array)

    def angle_between_radians(self, vector2):
        vector1_u = self.unit_vector()
        vector2_u = vector2.unit_vector()
        return np.arccos(np.clip(np.dot(vector1_u, vector2_u), -1.0, 1.0))

    def angle_between_degrees(self, vector2):
        radians = self.angle_between_radians(vector2)
        return np.degrees([radians.real])[0]
