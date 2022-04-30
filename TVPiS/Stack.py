import Log


class Stack:
    def __init__(self, mem_alloc, element_size=1):
        self.data = []
        self.mem_alloc = mem_alloc
        self.element_size = element_size

    def push(self, el):
        self.data.append(self.mem_alloc.alloc(self.element_size))
        # Save byte array to memory

    def pop(self):
        if len(self.data) > 0:
            el = self.data[-1]
            self.data = self.data[:-1]
            return el
        else:
            raise NameError(f'Stack has no elements')


class Queue:
    def __init__(self, mem_alloc, element_size=1):
        self.data = []
        self.mem_alloc = mem_alloc
        self.element_size = element_size

    def push(self, el):
        self.data.append(self.mem_alloc.alloc(self.element_size))
        # Save byte array to memory

    def peek(self):
        if len(self.data) > 0:
            return self.data[0]
        return None

    def pop(self):
        if len(self.data) > 0:
            el = self.data[0]
            self.data = self.data[1:]
            return el
        else:
            raise NameError(f'Queue has no elements')


class Deque:
    def __init__(self, mem_alloc, element_size=1):
        self.data = []
        self.mem_alloc = mem_alloc
        self.element_size = element_size

    def push_front(self, el):
        self.data.insert(0, self.mem_alloc.alloc(self.element_size))
        # Save byte array to memory

    def push_back(self, el):
        self.data.append(self.mem_alloc.alloc(self.element_size))
        # Save byte array to memory

    def peek_front(self):
        if len(self.data) > 0:
            return self.data[0]
        return None

    def peek_back(self):
        if len(self.data) > 0:
            return self.data[-1]
        return None

    def pop_front(self):
        if len(self.data) > 0:
            el = self.data[0]
            self.data = self.data[1:]
            return el
        else:
            raise NameError(f'Deque has no elements')

    def pop_back(self):
        if len(self.data) > 0:
            el = self.data[-1]
            self.data = self.data[0:-1]
            return el
        else:
            raise NameError(f'Deque has no elements')
