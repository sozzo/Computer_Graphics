class CyclicList:

    class Node:

        def __init__(self, value):
            self.value = value
            self.prev = self.next = None

    def __init__(self):
        self.current = None

    def empty(self):
        return self.current is None

    def push(self, value):
        new_node = self.Node(value)

        if self.empty():
            new_node.prev = new_node.next = new_node
            self.current = new_node
        else:
            new_node.prev = self.current
            new_node.next = self.current.next
            self.current.next.prev = new_node
            self.current.next = new_node
            self.current = new_node

        return self

    def pop(self):
        if self.empty():
            return None

        value = self.current.value

        if self.current == self.current.next:
            self.current = None
            return value

        self.current.prev.next = self.current.next
        self.current.next.prev = self.current.prev
        self.current = self.current.prev

        return self

    def move_back(self):
        self.current = self.current.prev
        return self

    def move_forward(self):
        self.current = self.current.next
        return self

    def to_list(self):
        result = []
        if self.current is None:
            return result

        start = self.current
        result.append(start.value)
        self.move_forward()

        while self.current != start:
            result.append(self.current.value)
            self.move_forward()

        return result