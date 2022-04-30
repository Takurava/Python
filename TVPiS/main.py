from MemAlloc import MemAlloc
from Stack import Stack
from Stack import Queue
from Stack import Deque


memAlloc = MemAlloc(1024)
print(memAlloc)

s1 = Stack(memAlloc, 1)
q1 = Queue(memAlloc, 2)
d1 = Deque(memAlloc, 4)

s1.push(bytes([3]))
s1.push(bytes([7]))
s1.push(bytes([0]))
q1.push(bytes([3]))
q1.push(bytes([7]))
q1.push(bytes([0]))
print(memAlloc)

print(s1.pop())
print(memAlloc)

print(q1.pop())
print(memAlloc)

d1.push_front(bytes([3]))
d1.push_front(bytes([7]))
d1.push_back(bytes([0]))
print(memAlloc)

d1.pop_front()
print(memAlloc)

d1.pop_back()
print(memAlloc)

d1.pop_back()
print(memAlloc)

try:
    d1.pop_front()
except Exception as ex:
    print(ex)
print(memAlloc)
