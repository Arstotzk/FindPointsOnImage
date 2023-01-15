import math

class Point(object):

    def __init__(self, _x, _y, _name, _template):
        self.X = _x
        self.Y = _y
        self.name = _name
        self.template = _template
        self.templateWidth, self.templateHeight = self.template.size
        self.pointOnImage = None

    def __init__(self, _name, _template):
        self.X = None
        self.Y = None
        self.name = _name
        self.template = _template
        self.templateWidth, self.templateHeight = self.template.size
        self.pointOnImage = None

    def setPointOnImage(self, _image):
        self.pointOnImage = _image
        self.pointOnImage.putpixel((self.X, self.Y), (0, 255, 0))

    def move(self, dx, dy):
        self.X = self.X + dx
        self.Y = self.Y + dy

    def __str__(self):
        return "Point(%s,%s)"%(self.X, self.Y)

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def setXY(self, _x, _y):
        self.X = _x
        self.Y = _y

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return math.hypot(dx, dy)