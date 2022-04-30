import Log


def fill_mem(mem_alloc, address, bytes_arr):
    segment = mem_alloc.segments[address.segment]
    for i in range(len(bytes_arr)):
        segment[i + address.addr] = bytes_arr[i]


class Stack:
    def __init__(self, mem_alloc, element_size=1):
        self.data = []
        self.mem_alloc = mem_alloc
        self.element_size = element_size

    def push(self, el):
        Log.save(f'Try to push to stack, Element = ({el})')
        if len(el) == self.element_size:
            el_address = self.mem_alloc.alloc(self.element_size)
            fill_mem(self.mem_alloc, el_address, el)
            self.data.append(el_address)
        else:
            raise NameError(f'Element size is {len(el)} bytes(s), stack element size is {self.element_size} byte(s)')

    def pop(self):
        Log.save(f'Try to pop from stack')
        if len(self.data) > 0:
            el_address = self.data[-1]
            self.data = self.data[:-1]
            el = self.mem_alloc.segments[el_address.segment][el_address.addr:(el_address.addr+self.element_size)]
            return el
        else:
            raise NameError(f'Stack has no elements')

    def __str__(self):
        date = [[self.mem_alloc.segments[e.segment][e.addr + i] for i in range(self.element_size)] for e in self.data]
        return f'Element size - {self.element_size}, date: {date}'


class Queue:
    def __init__(self, mem_alloc, element_size=1):
        self.data = []
        self.mem_alloc = mem_alloc
        self.element_size = element_size

    def push(self, el):
        Log.save(f'Try to push to queue, Element = ({el})')
        if len(el) == self.element_size:
            el_address = self.mem_alloc.alloc(self.element_size)
            fill_mem(self.mem_alloc, el_address, el)
            self.data.append(el_address)
        else:
            raise NameError(f'Element size is {len(el)} bytes(s), queue element size is {self.element_size} byte(s)')

    def peek(self):
        Log.save(f'Try to peek from queue')
        if len(self.data) > 0:
            el_address = self.data[0]
            el = self.mem_alloc.segments[el_address.segment][el_address.addr:(el_address.addr + self.element_size)]
            return el
        else:
            raise NameError(f'Queue has no elements')

    def pop(self):
        Log.save(f'Try to pop from queue')
        if len(self.data) > 0:
            el_address = self.data[0]
            self.data = self.data[1:]
            el = self.mem_alloc.segments[el_address.segment][el_address.addr:(el_address.addr + self.element_size)]
            return el
        else:
            raise NameError(f'Queue has no elements')

    def __str__(self):
        date = [[self.mem_alloc.segments[e.segment][e.addr + i] for i in range(self.element_size)] for e in self.data]
        return f'Element size - {self.element_size}, date: {date}'


class Deque:
    def __init__(self, mem_alloc, element_size=1):
        self.data = []
        self.mem_alloc = mem_alloc
        self.element_size = element_size

    def push_front(self, el):
        Log.save(f'Try to push front to deque, Element = ({el})')
        if len(el) == self.element_size:
            el_address = self.mem_alloc.alloc(self.element_size)
            fill_mem(self.mem_alloc, el_address, el)
            self.data.insert(0, el_address)
        else:
            raise NameError(f'Element size is {len(el)} bytes(s), deque element size is {self.element_size} byte(s)')

    def push_back(self, el):
        Log.save(f'Try to push back to deque, Element = ({el})')
        if len(el) == self.element_size:
            el_address = self.mem_alloc.alloc(self.element_size)
            fill_mem(self.mem_alloc, el_address, el)
            self.data.append(el_address)
        else:
            raise NameError(f'Element size is {len(el)} bytes(s), deque element size is {self.element_size} byte(s)')

    def peek_front(self):
        Log.save(f'Try to peek front from deque')
        if len(self.data) > 0:
            el_address = self.data[0]
            el = self.mem_alloc.segments[el_address.segment][el_address.addr:(el_address.addr + self.element_size)]
            return el
        else:
            raise NameError(f'Deque has no elements')

    def peek_back(self):
        Log.save(f'Try to peek back from deque')
        if len(self.data) > 0:
            el_address = self.data[-1]
            el = self.mem_alloc.segments[el_address.segment][el_address.addr:(el_address.addr + self.element_size)]
            return el
        else:
            raise NameError(f'Deque has no elements')

    def pop_front(self):
        Log.save(f'Try to pop front from deque')
        if len(self.data) > 0:
            el_address = self.data[0]
            self.data = self.data[1:]
            el = self.mem_alloc.segments[el_address.segment][el_address.addr:(el_address.addr + self.element_size)]
            return el
        else:
            raise NameError(f'Deque has no elements')

    def pop_back(self):
        Log.save(f'Try to pop back from deque')
        if len(self.data) > 0:
            el_address = self.data[-1]
            self.data = self.data[:-1]
            el = self.mem_alloc.segments[el_address.segment][el_address.addr:(el_address.addr + self.element_size)]
            return el
        else:
            raise NameError(f'Deque has no elements')

    def __str__(self):
        date = [[self.mem_alloc.segments[e.segment][e.addr + i] for i in range(self.element_size)] for e in self.data]
        return f'Element size - {self.element_size}, date: {date}'
