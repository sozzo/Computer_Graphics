from entities import Point
from graph import Graph
import graphics
from stripes_method import StripesMethod


class Main:
    width = 1000
    height = 700
    win = graphics.GraphWin("Stripes method", width, height)
    graph = None
    stripes_method = None
    last_point = None
    last_edges = []
    last_lines = []

    @staticmethod
    def on_right_click(event):
        if Main.graph is None:
            return
        if Main.last_point is not None:
            Main.last_point.undraw()
        for edge in Main.last_edges:
            edge.undraw()
            edge.draw(Main.win, "black")
            for vertex in [edge.source, edge.to]:
                vertex.undraw()
                vertex.draw(Main.win, "black")
        for line in Main.last_lines:
            line.undraw()

        Main.last_point = Point(event.x, Main.height - event.y)
        Main.last_point.draw(Main.win)
        result = Main.stripes_method.execute(Main.last_point)
        Main.last_edges = []
        Main.last_lines = []

        if result[0] is not None:
            for edge in result[0]:
                if edge is not None:
                    edge.undraw()
                    edge.draw(Main.win, "red")
                    for vertex in [edge.source, edge.to]:
                        vertex.undraw()
                        vertex.draw(Main.win, "red")
                    Main.last_edges.append(edge)
        for y in result[1]:
            if y is not None:
                line = graphics.Line(graphics.Point(0, y), graphics.Point(Main.width, y))
                line.setFill("blue")
                line.draw(Main.win)
                Main.last_lines.append(line)

    @staticmethod
    def main():
        Main.graph = Graph([("A", Point(560, 50)),
                           ("B", Point(240, 150)),
                           ("C", Point(800, 240)),
                           ("D", Point(500, 240)),
                           ("E", Point(80, 240)),
                           ("F", Point(480, 320)),
                           ("G", Point(900, 600)),
                           ("H", Point(100, 480)),
                           ("I", Point(640, 560)),
                           ("J", Point(160, 640))])

        Main.graph.add_edge("A", "B")
        Main.graph.add_edge("A", "C")
        Main.graph.add_edge("A", "D")
        Main.graph.add_edge("B", "D")
        Main.graph.add_edge("C", "G")
        Main.graph.add_edge("D", "E")
        Main.graph.add_edge("D", "F")
        Main.graph.add_edge("D", "G")
        Main.graph.add_edge("G", "I")
        Main.graph.add_edge("B", "E")
        Main.graph.add_edge("E", "H")
        Main.graph.add_edge("H", "J")
        Main.graph.add_edge("D", "J")
        Main.graph.add_edge("F", "J")
        Main.graph.add_edge("F", "I")
        Main.graph.add_edge("I", "J")

        Main.stripes_method = StripesMethod(Main.graph)

        Main.win.setCoords(0, 0, Main.width, Main.height)
        Main.graph.draw(Main.win)

        Main.win.bind('<Button-1>', Main.on_right_click)
        Main.win.mainloop()


if __name__ == '__main__':
    Main.main()
