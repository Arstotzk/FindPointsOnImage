from point import Points
from vector import Lines


class Param:

    def __init__(self, _name):
        self.name = _name
        self.min = None
        self.max = None
        self.value = None
        self.isFound = False
        self.isNormal = None

    def set_param(self, _min, _max, _value):
        self.min = _min
        self.max = _max
        self.value = _value
        self.isFound = True

        if _value < _min or _value > _max:
            self.isNormal = False
        else:
            self.isNormal = True


class Params:

    def __init__(self):
        self.FH_NA = Param("FN_NA")
        self.SNA = Param("SNA")
        self.ANB = Param("ANB")
        self.SN_A1AR = Param("SN_A1AR")
        self.SNB = Param("SNB")
        self.FH_NPg = Param("FH_NPg")
        self.IMPA = Param("IMPA")
        self.FMA = Param("FMA")

        self.all = [self.FH_NA, self.SNA, self.ANB, self.SN_A1AR, self.SNB, self.FH_NPg, self.IMPA, self.FMA]

    def calculate(self, _points, _lines):
        self.FH_NA.set_param(87, 93, _lines.FH.angle_between_degrees(_lines.NA))
        self.SNA.set_param(80, 84, _lines.SN.angle_between_degrees(_lines.NA.get_reverse()))
        self.ANB.set_param(0, 4, _lines.NB.angle_between_degrees(_lines.NA))
        self.SN_A1AR.set_param(99, 105, _lines.SN.angle_between_degrees(_lines.A1AR))
        self.SNB.set_param(78, 82, _lines.SN.angle_between_degrees(_lines.NB.get_reverse()))
        self.FH_NPg.set_param(87, 93, _lines.FH.angle_between_degrees(_lines.NPg))
        self.IMPA.set_param(86, 94, _lines.MP.angle_between_degrees(_lines.B1BR))
        # TODO: Fx
        self.FMA.set_param(21, 31, _lines.FH.angle_between_degrees(_lines.MP))

