import graphics
from entities import Point
from preparata_hull import PreparataHull
import utils


class Main:
    width = 1000
    height = 700
    win = graphics.GraphWin("Preparata convex hull", width, height)
    points = []
    hull = None

    @staticmethod
    def on_mouse_click(event):
        point = Point(event.x, event.y)
        if any(point.x == p.x and point.y == p.y for p in Main.points):
            return
        Main.points.append(point)
        point.draw(Main.win)

        if len(Main.points) > 2:
            if utils.are_collinear(Main.points):
                return
            if Main.hull is None:
                Main.hull = PreparataHull(Main.points)
            else:
                Main.hull.undraw(Main.win)
                Main.hull.add_point(point)

            Main.hull.draw(Main.win, "red")

    @staticmethod
    def main():
        Main.win.setMouseHandler(Main.on_mouse_click)
        Main.win.mainloop()


if __name__ == '__main__':
    Main.main()
