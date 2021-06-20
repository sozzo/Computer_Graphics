from cyclic_list import *
from entities import *
from utils import *


class GrahamsScan:

    @staticmethod
    def execute(points):
        first_point = min(points)
        result = CyclicList()

        for p in points:
            result.push(p)
        while result.current.value != first_point:
            result.move_forward()

        tail = result.current.prev.value
        stop = False

        while result.current.next.value != first_point or not stop:
            curr = result.current.value
            curr_next = result.current.next.value
            curr_next_next = result.current.next.next.value

            if curr_next == tail:
                stop = True
            if ccw(curr, curr_next, curr_next_next):
                result.move_forward()
            else:
                result.move_forward().pop()
                result.move_back()

        return ConvexHull(result.to_list())
