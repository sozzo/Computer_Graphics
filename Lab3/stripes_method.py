from bintrees import RBTree
import utils


class Stripe:
    def __init__(self, y, edges):
        self.y = y
        self.edges = edges

    def localize_point(self, point):
        left, right = self.__localize_point(0, len(self.edges), point)
        if left != -1 and right != len(self.edges):
            return self.edges[left], self.edges[right]
        elif left == -1:
            return None, self.edges[right]
        elif right == len(self.edges):
            return self.edges[left], None

    def __localize_point(self, left, right, point):
        if left == right:
            return left - 1, left

        mid = left + (right - left) // 2
        ccw = utils.ccw(self.edges[mid].source.point, self.edges[mid].to.point, point)

        if ccw > 0:
            return self.__localize_point(left, mid, point)
        if ccw < 0:
            if mid == left:
                return mid, mid + 1
            return self.__localize_point(mid, right, point)

        return mid, mid


class StripesMethod:
    def __init__(self, graph):
        self.stripes = []
        self.__sweep_graph(graph)

    def __sweep_graph(self, graph):
        tree = RBTree()
        last_y = -1

        for entry in graph.entries:
            if entry.vertex.point.y != last_y:
                self.stripes.append(Stripe(last_y, [edge for edge in tree]))
                last_y = entry.vertex.point.y

            for edge in entry.outbound_edges:
                tree.insert(edge, edge)
            for edge in entry.inbound_edges:
                tree.remove(edge)

        self.stripes.append(Stripe(last_y, []))

    def __find_stripe(self, left, right, point):
        if left == right:
            return left - 1

        mid = left + (right - left) // 2

        if point.y < self.stripes[mid].y:
            return self.__find_stripe(left, mid, point)
        else:
            if mid == left:
                return mid
            return self.__find_stripe(mid, right, point)

    def execute(self, point):
        stripe_num = self.__find_stripe(0, len(self.stripes), point)
        if stripe_num == 0:
            return None, (None, self.stripes[1].y)
        elif stripe_num == len(self.stripes) - 1:
            return None, (self.stripes[-1].y, None)
        return self.stripes[stripe_num].localize_point(point), (self.stripes[stripe_num].y,
                                                                self.stripes[stripe_num + 1].y)
