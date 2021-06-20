import graphics


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pict = graphics.Circle(graphics.Point(x, y), 3)
        self.set_color("black")

    def set_color(self, color):
        self.pict.setFill(color)
        self.pict.setOutline(color)

    def draw(self, window):
        self.pict.draw(window)

    def undraw(self):
        self.pict.undraw()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.y == other.y and self.x < other.x:
            return True
        return False

    def __gt__(self, other):
        return not self.__lt__(other)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)
