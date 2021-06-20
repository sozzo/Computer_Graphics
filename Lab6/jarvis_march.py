from entities import *
from utils import *


class JarvisMarch:

    @staticmethod
    def execute(points):
        hull_points = []
        lowest_point = min(points)
        highest_point = max(points)

        hull_points.append(lowest_point)
        new_point = min(points, key=lambda p: polar_angle(lowest_point, p) if lowest_point != p else math.inf)

        while new_point != highest_point:
            hull_points.append(new_point)
            new_point = min(points, key=lambda p: polar_angle(new_point, p) if new_point != p else math.inf)

        origin = Point(0, 0)
        while new_point != lowest_point:
            hull_points.append(new_point)
            new_point = min(points, key=lambda p: polar_angle(origin - new_point, origin - p)
                            if new_point != p else math.inf)

        return ConvexHull(hull_points)
