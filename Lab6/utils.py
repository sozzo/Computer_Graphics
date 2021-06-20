from entities import Point
import math


def length(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def euclidean_norm(v):
    return math.sqrt(v.x * v.x + v.y * v.y)


def polar_angle(origin, point):
    x = point.x - origin.x
    y = point.y - origin.y

    if x > 0:
        if y >= 0:
            return math.atan(y / x)
        else:
            return 2 * math.pi + math.atan(y / x)
    elif x < 0:
        return math.pi + math.atan(y / x)
    else:
        if y > 0:
            return math.pi / 2
        elif y < 0:
            return 3 * math.pi / 2
        else:
            return None


def ccw(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x) > 0


def centroid(points):
    x_average = 0
    y_average = 0
    for p in points:
        x_average += p.x
        y_average += p.y
    x_average /= len(points)
    y_average /= len(points)
    return Point(x_average, y_average)


def belongs_to_convex_polygon(polygon_points, point):
    left, right = 1, len(polygon_points) - 1

    if not ccw(polygon_points[0], polygon_points[left], point) or \
            ccw(polygon_points[0], polygon_points[right], point):
        return False

    while right - left > 1:
        mid = left + (right - left) // 2
        if not ccw(polygon_points[0], polygon_points[mid], point):
            right = mid
        else:
            left = mid

    return ccw(polygon_points[left], polygon_points[right], point)


# on the left: <0, on the right: >0, otherwise belongs to line
def check_side(p1, p2, point):
    return (point.x - p1.x) * (p2.y - p1.y) - (point.y - p1.y) * (p2.x - p1.x)


def dot_product(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


def find_cos(v1, v2):
    return dot_product(v1, v2) / (euclidean_norm(v1) * euclidean_norm(v2))
