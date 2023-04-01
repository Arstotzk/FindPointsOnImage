from point import Points
from vector import Lines


class Param:

    def __init__(self, _name, _guid):
        self.name = _name
        self.min = None
        self.max = None
        self.value = None
        self.isFound = False
        self.isNormal = None
        self.typeGuid = _guid
        self.guid = None

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
        self.FH_NA = Param("FN_NA", "33a9bc9c-142a-4f2a-bbec-3da33e17e29f")
        self.SNA = Param("SNA", "c6e1982a-861b-4588-919d-ff5d5c2faeec")
        self.ANB = Param("ANB", "eff8fb0a-68c3-4477-a43f-5cb97e4b163c")
        self.SN_A1AR = Param("SN_A1AR", "01b5f198-3c26-47a6-ba55-be576a24d921")
        self.SNB = Param("SNB", "7b8e2708-cdb3-4988-b6d2-fb5f703ce598")
        self.FH_NPg = Param("FH_NPg", "c78c136d-6536-4d45-bef3-957c83512d9e")
        self.IMPA = Param("IMPA", "12941443-33fa-4c45-9398-0ad0ea08edea")
        self.FMA = Param("FMA", "11d8c727-122b-4e04-bda9-c3c3ccebf133")

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

