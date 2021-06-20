from entities import Point, Segment
import graphics
import utils


class Vertex:
    def __init__(self, number, point, label):
        self.number = number
        self.point = point
        self.label = label
        self.label_pict = graphics.Text(graphics.Point(point.x + 13, point.y + 5), label)

    def __lt__(self, other):
        if self.point.y < other.point.y:
            return True
        elif self.point.y == other.point.y and self.point.x < other.point.x:
            return True
        return False

    def __gt__(self, other):
        return not self < other

    def draw(self, window, color):
        self.point.set_color(color)
        self.point.draw(window)
        self.label_pict.setFill(color)
        self.label_pict.draw(window)

    def undraw(self):
        self.point.undraw()
        self.label_pict.undraw()

    def __eq__(self, other):
        return self.point == other.point


class Edge:
    def __init__(self, source, to):
        self.source = source
        self.to = to
        self.segment = Segment(source.point, to.point)

    def __eq__(self, other):
        return self.source == other.source and self.to == other.to

    def __lt__(self, other):
        if self.source.point != other.source.point and self.to.point != other.to.point:
            line_level = max(self.source.point.y, other.source.point.y)
            line_p1 = Point(0, line_level)
            line_p2 = Point(1, line_level)
            x_self, _ = utils.intersect(self.source.point, self.to.point, line_p1, line_p2)
            x_other, _ = utils.intersect(other.source.point, other.to.point, line_p1, line_p2)
            if x_self is None:
                x_self = self.source.point.x
            if x_other is None:
                x_other = self.to.point.x
            return x_self < x_other

        if self.source.point == other.source.point:
            origin = self.source.point
            self_angle = utils.polar_angle(origin, self.to.point)
            other_angle = utils.polar_angle(origin, other.to.point)
            return self_angle > other_angle
        else:
            origin = self.to.point
            self_angle = utils.polar_angle(origin, self.source.point)
            other_angle = utils.polar_angle(origin, other.source.point)
            return self_angle < other_angle

    def __gt__(self, other):
        if self.source.point != other.source.point and self.to.point != other.to.point:
            line_level = max(self.source.point.y, other.source.point.y)
            line_p1 = Point(0, line_level)
            line_p2 = Point(1, line_level)
            x_self, _ = utils.intersect(self.source.point, self.to.point, line_p1, line_p2)
            x_other, _ = utils.intersect(other.source.point, other.to.point, line_p1, line_p2)
            if x_self is None:
                x_self = self.source.point.x
            if x_other is None:
                x_other = self.to.point.x
            return x_self > x_other

        if self.source.point == other.source.point:
            origin = self.source.point
            self_angle = utils.polar_angle(origin, self.to.point)
            other_angle = utils.polar_angle(origin, other.to.point)
            return self_angle < other_angle
        else:
            origin = self.to.point
            self_angle = utils.polar_angle(origin, self.source.point)
            other_angle = utils.polar_angle(origin, other.source.point)
            return self_angle > other_angle

    def draw(self, window, color):
        self.segment.set_color(color)
        self.segment.draw(window)

    def undraw(self):
        self.segment.undraw()


class Entry:
    def __init__(self, vertex):
        self.vertex = vertex
        self.inbound_edges = []
        self.outbound_edges = []

    def draw(self, window, vertex_color, edge_color):
        for edge in self.outbound_edges:
            edge.draw(window, edge_color)
        self.vertex.draw(window, vertex_color)


class Graph:
    def __init__(self, labeled_points):
        self.entries = []
        for label, point in labeled_points:
            self.entries.append(Entry(Vertex(0, point, label)))
        self.entries.sort(key=lambda entry: entry.vertex)
        for i in range(len(self.entries)):
            self.entries[i].vertex.number = i

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

        mid = left + (right - left) // 2

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
