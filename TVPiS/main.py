from MemAlloc import MemAlloc
from Stack import Stack
from Stack import Queue
from Stack import Deque


memAlloc = MemAlloc(1024)
print(memAlloc)

s1 = Stack(memAlloc, 1)
q1 = Queue(memAlloc, 2)
d1 = Deque(memAlloc, 4)

s1.push(bytes('o', 'utf8'))
s1.push(bytes('t', 'utf8'))
s1.push(bytes('f', 'utf8'))
q1.push(bytes('se', 'utf8'))
q1.push(bytes('nr', 'utf8'))
q1.push(bytes('pm', 'utf8'))
print(memAlloc)
print(s1)
print(q1)

print(s1.pop())
print(memAlloc)
print(s1)

print(q1.pop())
print(memAlloc)
print(q1)

d1.push_front(bytes('fuck', 'utf8'))
d1.push_front(bytes('duck', 'utf8'))
d1.push_back(bytes('suck', 'utf8'))
print(memAlloc)
print(d1)

print(d1.pop_front())
print(memAlloc)
print(d1)

print(d1.pop_back())
print(memAlloc)
print(d1)

print(d1.pop_back())
print(memAlloc)
print(d1)

try:
    print(d1.pop_front())
except Exception as ex:
    print(ex)
print(memAlloc)
print(d1)
