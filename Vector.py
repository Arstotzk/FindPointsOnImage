import math
import point
import numpy as np


class Vec2:

    def __init__(self, _name):
        self.pointStart = None
        self.pointEnd = None
        self.X = None
        self.Y = None
        self.array = [None, None]
        self.name = _name

    def set_vector(self, _point_start, _point_end):
        self.pointStart = _point_start
        self.pointEnd = _point_end
        self.X = _point_end.X - _point_start.X
        self.Y = _point_end.Y - _point_start.Y
        self.array = [self.X, self.Y]

    def get_reverse(self):
        reverse_vector = Vec2(''.join(reversed(self.name)))
        reverse_vector.pointEnd = self.pointStart
        reverse_vector.pointStart = self.pointEnd
        reverse_vector.X = - self.X
        reverse_vector.Y = - self.Y
        reverse_vector.array = [reverse_vector.X, reverse_vector.Y]
        return reverse_vector

    def unit_vector(self):
        return self.array / np.linalg.norm(self.array)

    def angle_between_radians(self, vector2):
        vector1_u = self.unit_vector()
        vector2_u = vector2.unit_vector()
        return np.arccos(np.clip(np.dot(vector1_u, vector2_u), -1.0, 1.0))

    def angle_between_degrees(self, vector2):
        radians = self.angle_between_radians(vector2)
        return np.degrees([radians.real])[0]


class Lines:

    def __init__(self):
        self.FH = Vec2("FH")
        self.NA = Vec2("NA")
        self.NB = Vec2("NB")
        self.SN = Vec2("SN")
        self.A1AR = Vec2("A1AR")
        self.NPg = Vec2("NPg")
        self.MP = Vec2("MP")
        self.B1BR = Vec2("B1BR")

        self.all = [self.FH, self.NA, self.NB, self.SN, self.A1AR, self.NPg, self.MP, self.B1BR]

    def calculate(self, _points):
        self.FH.set_vector(_points.Or, _points.Po)
        self.NA.set_vector(_points.N, _points.A)
        self.NB.set_vector(_points.N, _points.B)
        self.SN.set_vector(_points.S, _points.N)
        self.A1AR.set_vector(_points.A1, _points.AR)
        self.NPg.set_vector(_points.N, _points.Pg)
        self.MP.set_vector(_points.Me, _points.Go)
        self.B1BR.set_vector(_points.B1, _points.BR)
