import graphics
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pict = graphics.Circle(graphics.Point(x, y), 3)
        self.set_color("black")

    def set_color(self, color):
        self.pict.setFill(color)
        self.pict.setOutline(color)

    def set_width(self, width):
        self.pict.setWidth(width)

    def draw(self, window):
        self.pict.draw(window)

    def undraw(self):
        self.pict.undraw()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.pict = graphics.Line(graphics.Point(p1.x, p1.y), graphics.Point(p2.x, p2.y))
        self.set_color("black")

    def set_color(self, color):
        self.pict.setFill(color)
        self.pict.setOutline(color)

    def draw(self, window):
        self.pict.draw(window)

    def undraw(self):
        self.pict.undraw()

    def __lt__(self, other):
        mid_self = (self.p1.x + self.p2.x) / 2
        mid_other = (other.p1.x + other.p2.x) / 2
        if mid_self < mid_other:
            return True
        return False

    def __gt__(self, other):
        return not self.__lt__(other)
