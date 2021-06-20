from enum import Enum
import graphics
import math
import utils


class PreparataHull:

    class PointStatus(Enum):
        CONVEX = 0
        CONCAVE = 1
        TANGENT = 2

    def __init__(self, points):
        self.points = points.copy()
        self.__sort_points()
        self.lines = []

    def __sort_points(self):
        centroid = utils.centroid(self.points)
        self.points.sort(key=lambda p: utils.polar_angle(centroid, p))

    def add_point(self, point):
        left_segment, right_segment = self.__find_segments(0, len(self.points) - 1, point)
        if left_segment is None:
            return
        left_tangent = self.__find_tangent(left_segment[0], left_segment[1], point, True)
        right_tangent = self.__find_tangent(right_segment[0], right_segment[1], point, False)

        if right_tangent < left_tangent:
            self.points = [point] + self.points[right_tangent:left_tangent + 1]
        else:
            self.points = [point] + self.points[right_tangent:] + self.points[:left_tangent + 1]

    def __check_status(self, point, vertex_index):
        vertex = self.points[vertex_index]
        left_neighbour = self.points[vertex_index - 1]
        right_neighbour = self.points[(vertex_index + 1) % len(self.points)]

        ccw1 = utils.ccw(point, vertex, left_neighbour)
        ccw2 = utils.ccw(point, vertex, right_neighbour)

        if ccw1 * ccw2 > 0:
            # neighbours lie on the same side
            return PreparataHull.PointStatus.TANGENT
        elif ccw1 > 0:
            return PreparataHull.PointStatus.CONVEX
        return PreparataHull.PointStatus.CONCAVE

    def __find_segments(self, left, right, point):
        if left >= right:
            return None, None

        mid = left + (right - left) // 2

        angle = utils.angle(self.points[left], point, self.points[mid])
        status_left = self.__check_status(point, left)
        status_mid = self.__check_status(point, mid)

        if angle <= math.pi:
            if status_left == PreparataHull.PointStatus.CONCAVE:
                if status_mid == PreparataHull.PointStatus.CONCAVE:
                    # case 1
                    return self.__find_segments(mid + 1, right, point)
                else:
                    # case 2
                    return (left, mid), (mid + 1, right)
            else:
                if status_mid == PreparataHull.PointStatus.CONVEX:
                    # case 3
                    return self.__find_segments(left, mid - 1, point)
                else:
                    # case 4
                    if mid == left:
                        return (left, mid), (mid + 1, right)
                    return (mid, right), (left, mid - 1)
        else:
            if status_left == PreparataHull.PointStatus.CONVEX:
                if status_mid == PreparataHull.PointStatus.CONVEX:
                    # case 5
                    return self.__find_segments(mid + 1, right, point)
                else:
                    # case 6
                    return (mid + 1, right), (left, mid)
            else:
                if status_mid == PreparataHull.PointStatus.CONCAVE:
                    # case 7
                    return self.__find_segments(left, mid - 1, point)
                else:
                    # case 8
                    return (left, mid - 1), (mid, right)

    def __find_tangent(self, left, right, point, left_tangent=True):
        if left > right:
            return None

        mid = left + (right - left) // 2
        status = self.__check_status(point, mid)

        if status == PreparataHull.PointStatus.TANGENT:
            return mid
        elif status == PreparataHull.PointStatus.CONVEX:
            if left_tangent:
                return self.__find_tangent(left, mid - 1, point, left_tangent)
            else:
                return self.__find_tangent(mid + 1, right, point, left_tangent)
        else:
            if left_tangent:
                return self.__find_tangent(mid + 1, right, point, left_tangent)
            else:
                return self.__find_tangent(left, mid - 1, point, left_tangent)

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
