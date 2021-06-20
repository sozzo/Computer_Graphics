import entities
import math


def centroid(points):
    x_average = 0
    y_average = 0
    for p in points:
        x_average += p.x
        y_average += p.y
    x_average /= len(points)
    y_average /= len(points)
    return entities.Point(x_average, y_average)


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


def angle(p1, p2, p3):
    angle1 = polar_angle(p2, p3)
    angle2 = polar_angle(p2, p1)
    diff = angle1 - angle2
    if diff >= 0:
        return diff
    else:
        return 2 * math.pi + diff


# >0 if counterclockwise ("left turn"), =0 if collinear, <0 if clockwise ("right turn")
def ccw(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)


def are_collinear(points):
    for i in range(len(points) - 2):
        if ccw(points[i], points[i + 1], points[i + 2]) == 0:
            return True
    return False
