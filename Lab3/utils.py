import math


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


def intersect(p11, p12, p21, p22):
    if p11.x == p12.x or p21.x == p22.x:
        return None, None

    k1 = (p12.y - p11.y) / (p12.x - p11.x)
    b1 = p11.y - k1 * p11.x
    k2 = (p22.y - p21.y) / (p22.x - p21.x)
    b2 = p21.y - k2 * p21.x

    if k1 == k2:
        return None, None
    x = (b2 - b1) / (k1 - k2)
    y = k1 * x + b1
    return x, y


# >0 if counterclockwise ("left turn"), =0 if collinear, <0 if clockwise ("right turn")
def ccw(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
