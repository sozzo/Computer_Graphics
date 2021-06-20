import time

from entities import *
from grahams_scan import GrahamsScan
from jarvis_march import JarvisMarch
from utils import *


class DivideAndConquerAlgorithm:
    min_points = 6
    win = None

    @staticmethod
    def execute(points, window):
        DivideAndConquerAlgorithm.win = window
        return DivideAndConquerAlgorithm.__recursive_merge(points, 0, len(points) - 1)

    @staticmethod
    def __recursive_merge(points, left, right):
        if right - left + 1 <= DivideAndConquerAlgorithm.min_points:
            return JarvisMarch.execute([points[i] for i in range(left, right + 1)])

        hull1 = DivideAndConquerAlgorithm.__recursive_merge(points, left, left + (right - left) // 2)
        hull2 = DivideAndConquerAlgorithm.__recursive_merge(points, left + (right - left) // 2 + 1, right)

        hull1.draw(DivideAndConquerAlgorithm.win, "blue")
        hull2.draw(DivideAndConquerAlgorithm.win, "green")
        time.sleep(1)
        hull1.undraw(DivideAndConquerAlgorithm.win)
        hull2.undraw(DivideAndConquerAlgorithm.win)

        pivot = centroid(hull1.points)

        if belongs_to_convex_polygon(hull2.points, pivot):
            merged_points = DivideAndConquerAlgorithm.__merge_hulls(hull1, hull2, pivot)
        else:
            index1, index2 = DivideAndConquerAlgorithm.__find_tangents_to_hull(pivot, hull2)
            hull2_points_to_merge = DivideAndConquerAlgorithm.__get_sublist(hull2.points, index1, index2)
            merged_points = DivideAndConquerAlgorithm.__merge_hulls(hull1, ConvexHull(hull2_points_to_merge), pivot)

        return GrahamsScan.execute(merged_points)

    @staticmethod
    def __find_tangents_to_hull(point, hull):
        pivot = centroid(hull.points)
        v1 = pivot - point
        min_cos_left = min_cos_right = 2
        left_index = right_index = 0

        for i in range(len(hull.points)):
            cos = find_cos(v1, hull.points[i] - point)
            if check_side(point, pivot, hull.points[i]) < 0:
                if cos < min_cos_left:
                    min_cos_left = cos
                    left_index = i
            else:
                if cos < min_cos_right:
                    min_cos_right = cos
                    right_index = i

        return right_index, left_index

    @staticmethod
    def __get_sublist(this_list, start_index, end_index):
        result = []

        if start_index < end_index:
            for i in range(start_index, end_index + 1):
                result.append(this_list[i])
        else:
            for i in range(start_index, len(this_list)):
                result.append(this_list[i])
            for i in range(end_index + 1):
                result.append(this_list[i])

        return result

    @staticmethod
    def __merge_hulls(hull1, hull2, pivot):
        sorted_points = []
        i, j = 0, 0

        min_angle_point1 = min(hull1.points, key=lambda p: polar_angle(pivot, p))
        shift1 = list.index(hull1.points, min_angle_point1)
        min_angle_point2 = min(hull2.points, key=lambda p: polar_angle(pivot, p))
        shift2 = list.index(hull2.points, min_angle_point2)

        while i < len(hull1.points) and j < len(hull2.points):
            i_shifted = (i + shift1) % len(hull1.points)
            j_shifted = (j + shift2) % len(hull2.points)
            angle1 = polar_angle(pivot, hull1.points[i_shifted])
            angle2 = polar_angle(pivot, hull2.points[j_shifted])

            if angle1 < angle2:
                sorted_points.append(hull1.points[i_shifted])
                i += 1
            elif angle1 > angle2:
                sorted_points.append(hull2.points[j_shifted])
                j += 1
            else:
                dist1 = length(pivot, hull1.points[i_shifted])
                dist2 = length(pivot, hull2.points[j_shifted])

                if dist1 < dist2:
                    sorted_points.append(hull1.points[i_shifted])
                    i += 1
                else:
                    sorted_points.append(hull2.points[j_shifted])
                    j += 1

        while i < len(hull1.points):
            sorted_points.append(hull1.points[(i + shift1) % len(hull1.points)])
            i += 1
        while j < len(hull2.points):
            sorted_points.append(hull2.points[(j + shift2) % len(hull2.points)])
            j += 1

        return sorted_points
