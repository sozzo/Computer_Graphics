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


class ConvexHull:

    def __init__(self, points):
        self.points = points
        self.lines = []

    def __build_lines(self):
        self.lines.clear()
        for i in range(len(self.points)):
            current_point = self.points[i]
            next_point = self.points[(i + 1) % len(self.points)]
            self.lines.append(graphics.Line(graphics.Point(current_point.x, current_point.y),
                                            graphics.Point(next_point.x, next_point.y)))
            self.lines[i].setWidth(2)

    def draw(self, window, color):
        self.__build_lines()
        for line in self.lines:
            line.setFill(color)
            line.setOutline(color)
            line.draw(window)
        for point in self.points:
            point.undraw()
            point.set_color(color)
            point.draw(window)

    def undraw(self, window):
        for line in self.lines:
            line.undraw()
        for point in self.points:
            point.undraw()
            point.set_color("black")
            point.draw(window)
