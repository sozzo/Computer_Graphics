import graphics
import math
from math import pi
from sympy.geometry import *


class Vertex:
    def __init__(self, number, label, point):
        self.number = number
        self.label = label
        self.point = point
        self.pointWidth = 3
        self.pictPoint = graphics.Circle(graphics.Point(point.x, point.y), self.pointWidth)
        self.pictLabel = graphics.Text(graphics.Point(point.x + self.pointWidth + 10, point.y), label)

    def __lt__(self, other):
        if self.point.y < other.point.y:
            return True
        elif self.point.y == other.point.y and self.point.x < other.point.x:
            return True
        return False

    def __repr__(self):
        return "[" + self.label + ", (" + str(self.point.x) + ", " + str(self.point.y) + ")]"

    def draw(self, window, color):
        self.pictPoint.setFill(color)
        self.pictPoint.setOutline(color)
        self.pictPoint.draw(window)
        self.pictLabel.draw(window)

    def undraw(self):
        self.pictPoint.undraw()
        self.pictLabel.undraw()


class Edge:
    def __init__(self, source, to):
        self.source = source
        self.to = to
        self.weight = 1
        self.segment = Segment(source.point, to.point)
        self.pictLine = graphics.Line(graphics.Point(source.point.x, source.point.y),
                                      graphics.Point(to.point.x, to.point.y))

    def __lt__(self, other):
        horizontal = Line(Point(0, 0), Point(1, 0))
        self_angle = self.segment.angle_between(horizontal)
        other_angle = other.segment.angle_between(horizontal)
        return self_angle > other_angle

    def __gt__(self, other):
        horizontal = Line(Point(0, 0), Point(1, 0))
        self_angle = self.segment.angle_between(horizontal)
        other_angle = other.segment.angle_between(horizontal)
        return self_angle < other_angle

    def __repr__(self):
        return "[to: " + str(self.to.label) + ", weight: " + str(self.weight) + "]"

    def draw(self, window, color):
        self.pictLine.setFill(color)
        self.pictLine.setOutline(color)
        self.pictLine.draw(window)

    def undraw(self):
        self.pictLine.undraw()


class Entry:
    def __init__(self, vertex):
        self.vertex = vertex
        self.inbound_edges = []
        self.outbound_edges = []

    def __repr__(self):
        result = str(self.vertex) + ": "
        for j in range(len(self.outbound_edges)):
            result += str(self.outbound_edges[j])
            if j != len(self.outbound_edges) - 1:
                result += ", "
        return result + "\n"

    def draw(self, window, vertex_color, edge_color):
        for edge in self.outbound_edges:
            edge.draw(window, edge_color)
        self.vertex.draw(window, vertex_color)


class Graph:
    def __init__(self, vertices):
        self.entries = []
        for p in vertices:
            self.entries.append(Entry(Vertex(0, p[0], p[1])))
        self.entries.sort(key=lambda entry: entry.vertex)
        for i in range(len(self.entries)):
            self.entries[i].vertex.number = i

    def __repr__(self):
        result = ""
        for entry in self.entries:
            result += str(entry)
        return result

    def add_edge(self, source_label, to_label):
        source = 0
        to = 0

        for entry in self.entries:
            if entry.vertex.label == source_label:
                source = entry.vertex.number
                break
        for entry in self.entries:
            if entry.vertex.label == to_label:
                to = entry.vertex.number
                break

        if source == to:
            return
        if source > to:
            source, to = to, source

        edge = Edge(self.entries[source].vertex, self.entries[to].vertex)
        outbound = self.entries[source].outbound_edges
        inbound = self.entries[to].inbound_edges

        self.__insert_edge(edge, outbound, False)
        self.__insert_edge(edge, inbound, True)

    def __insert_edge(self, new_edge, edges, inbound):
        index = self.__find_position(edges, new_edge, 0, len(edges))
        if inbound:
            index = len(edges) - index

        if index > -1:
            if index < len(edges):
                edges.insert(index, new_edge)
            else:
                edges.append(new_edge)

    def __find_position(self, edges, new_edge, left, right):
        if left == right:
            return left

        mid = math.floor((left + right) / 2)

        if edges[mid] > new_edge:
            return self.__find_position(edges, new_edge, left, mid)
        if edges[mid] < new_edge:
            if mid == left:
                return mid + 1
            return self.__find_position(edges, new_edge, mid, right)

        return -1

    def draw(self, window):
        for entry in self.entries:
            entry.draw(window, "black", "black")


class Chain:
    def __init__(self, edges):
        self.edges = edges
        self.monotonous_line = self.__build_monotonous_line()
        self.projected_vertices = self.__project_vertices(self.monotonous_line)
        self.reversed = False

        if Chain.__compare_on_line(self.projected_vertices[0], self.projected_vertices[1]) > 0:
            self.projected_vertices.reverse()
            self.reversed = True

    def __repr__(self):
        result = ""
        for edge in self.edges:
            result += edge.source.label + " -> "
        return result + self.edges[-1].to.label

    def __build_monotonous_line(self):
        point = Point(1000, 0)
        angle = pi/2
        line = Line(point, Point(1000, 1000))
        found = False

        while not found:
            found = True
            for edge in self.edges:
                if line.is_perpendicular(edge.segment):
                    angle -= 10e-2
                    line = Line(point, slope=angle)
                    found = False
                    break

        return line

    def discriminate(self, point):
        projected_point = self.monotonous_line.projection(point)

        to_index = self.__localize_point(projected_point, 0, len(self.projected_vertices))
        if self.reversed:
            to_index = len(self.projected_vertices) - to_index

        if to_index == 0:
            end_line = self.monotonous_line.parallel_line(self.edges[0].source.point)
            return Chain.__check_side(point, end_line)
        if to_index == len(self.projected_vertices):
            end_line = self.monotonous_line.parallel_line(self.edges[-1].to.point)
            return Chain.__check_side(point, end_line)
        return Chain.__check_side(point, self.edges[to_index - 1].segment)

    def __project_vertices(self, line):
        projected = []
        for edge in self.edges:
            projected.append(line.projection(edge.source.point))
        projected.append(line.projection(self.edges[-1].to.point))
        return projected

    def __localize_point(self, point, left, right):
        if left == right:
            return left

        mid = math.floor((left + right) / 2)

        if Chain.__compare_on_line(self.projected_vertices[mid], point) < 0:
            if mid == left:
                return mid + 1
            return self.__localize_point(point, mid, right)

        return self.__localize_point(point, left, mid)

    @staticmethod
    def __compare_on_line(left, right):
        sum_left = left.x + left.y
        sum_right = right.x + right.y
        return sum_left - sum_right

    @staticmethod
    def __check_side(point, linear_entity):
        p1 = linear_entity.p1
        p2 = linear_entity.p2
        return (point.x - p1.x) * (p2.y - p1.y) - (point.y - p1.y) * (p2.x - p1.x)

    def draw(self, window, color):
        for edge in self.edges:
            edge.undraw()
            edge.source.undraw()
            edge.to.undraw()
            edge.draw(window, color)
            edge.source.draw(window, "black")
            edge.to.draw(window, "black")

    def undraw(self, window):
        for edge in self.edges:
            edge.undraw()
            edge.source.undraw()
            edge.to.undraw()
            edge.draw(window, "black")
            edge.source.draw(window, "black")
            edge.to.draw(window, "black")


class ChainsMethod:
    def __init__(self, graph):
        self.graph = graph
        self.chains = []
        self.__build_chains()

    def __build_chains(self):
        self.__balance_by_weights()

        for init_edge in self.graph.entries[0].outbound_edges:
            while init_edge.weight != 0:
                edges_path = [init_edge]
                init_edge.weight -= 1
                current_vertex = init_edge.to.number

                while current_vertex != self.graph.entries[-1].vertex.number:
                    for edge in self.graph.entries[current_vertex].outbound_edges:
                        if edge.weight != 0:
                            edges_path.append(edge)
                            edge.weight -= 1
                            current_vertex = edge.to.number
                            break

                self.chains.append(Chain(edges_path))

    def __balance_by_weights(self):
        for i in range(1, len(self.graph.entries) - 1):
            w_in = self.__weights_in(i)
            w_out = self.__weights_out(i)
            if w_in > w_out:
                self.graph.entries[i].outbound_edges[0].weight = w_in - w_out + 1

        for i in range(len(self.graph.entries) - 2, 0, -1):
            w_in = self.__weights_in(i)
            w_out = self.__weights_out(i)
            if w_out > w_in:
                self.graph.entries[i].inbound_edges[0].weight = w_out - w_in + 1

    def __weights_in(self, i):
        total = 0
        for edge in self.graph.entries[i].inbound_edges:
            total += edge.weight
        return total

    def __weights_out(self, i):
        total = 0
        for edge in self.graph.entries[i].outbound_edges:
            total += edge.weight
        return total

    def localize_point(self, point):
        index = self.__find_chain(point, 0, len(self.chains))
        if index < len(self.chains):
            if self.chains[index].discriminate(point) == 0:
                return self.chains[index], None
        if index == 0 or index == len(self.chains):
            return None
        return self.chains[index - 1], self.chains[index]

    def __find_chain(self, point, left, right):
        if left == right:
            return left

        mid = math.floor((left + right) / 2)
        ind = self.chains[mid].discriminate(point)

        if ind < 0:
            return self.__find_chain(point, left, mid)
        if ind > 0:
            if mid == left:
                return mid + 1
            return self.__find_chain(point, mid, right)

        return mid


def on_window_click(event):
    if on_window_click.lastPoint is not None:
        on_window_click.lastPoint.undraw()
        if on_window_click.lastChains is not None:
            for chain in on_window_click.lastChains:
                if chain is not None:
                    chain.undraw(on_window_click.window)

    on_window_click.lastPoint = graphics.Circle(graphics.Point(event.x, 700 - event.y), 3)
    on_window_click.lastPoint.setFill("red")
    on_window_click.lastPoint.setOutline("red")
    on_window_click.lastPoint.draw(on_window_click.window)

    result = on_window_click.chainsMethod.localize_point(Point(event.x, 700 - event.y))
    if result is not None:
        result[0].draw(on_window_click.window, "red")
        if result[1] is not None:
            result[1].draw(on_window_click.window, "red")
    on_window_click.lastChains = result


on_window_click.window = None
on_window_click.lastPoint = None
on_window_click.lastChains = None
on_window_click.chainsMethod = None


def test():
    the_graph = Graph([("A", Point(560, 50)),
                       ("B", Point(240, 150)),
                       ("C", Point(700, 170)),
                       ("D", Point(400, 240)),
                       ("E", Point(80, 240)),
                       ("F", Point(480, 320)),
                       ("G", Point(720, 400)),
                       ("H", Point(100, 480)),
                       ("I", Point(640, 560)),
                       ("J", Point(160, 640))])

    the_graph.add_edge("A", "B")
    the_graph.add_edge("A", "C")
    the_graph.add_edge("A", "D")
    the_graph.add_edge("B", "D")
    the_graph.add_edge("C", "G")
    the_graph.add_edge("D", "F")
    the_graph.add_edge("D", "G")
    the_graph.add_edge("G", "I")
    the_graph.add_edge("B", "E")
    the_graph.add_edge("E", "H")
    the_graph.add_edge("H", "J")
    the_graph.add_edge("D", "J")
    the_graph.add_edge("F", "J")
    the_graph.add_edge("F", "I")
    the_graph.add_edge("I", "J")

    win = graphics.GraphWin("Chains Method", 800, 700)
    win.setCoords(0, 0, 800, 700)

    the_graph.draw(win)
    on_window_click.window = win
    on_window_click.chainsMethod = ChainsMethod(the_graph)
    for chain in on_window_click.chainsMethod.chains:
        print(chain)

    win.bind('<Button-1>', on_window_click)
    win.mainloop()


if __name__ == '__main__':
    test()
