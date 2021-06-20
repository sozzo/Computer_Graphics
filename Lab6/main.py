import graphics
from divide_and_conquer import DivideAndConquerAlgorithm
from entities import Point


class Main:
    width = 1000
    height = 700
    win = graphics.GraphWin("Divide And Conquer!", width, height)
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
            if Main.hull is not None:
                Main.hull.undraw(Main.win)
            Main.hull = DivideAndConquerAlgorithm.execute(Main.points, Main.win)
            Main.hull.draw(Main.win, "red")

    @staticmethod
    def main():
        Main.win.setMouseHandler(Main.on_mouse_click)
        Main.win.mainloop()


if __name__ == '__main__':
    Main.main()
