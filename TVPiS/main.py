from MemAlloc import MemAlloc
from Hash import Hash


memAlloc = MemAlloc(1024)
print(memAlloc)

h = Hash(memAlloc)

h.update('me', bytes('o', 'utf8'))
print(h)
print(memAlloc)
print(h.get('me'))
print(h.get_guts())

h.update('me', bytes('oo', 'utf8'))
h.update('he', bytes('vt', 'utf8'))
h.update('ie', bytes('hy', 'utf8'))
h.update('pe', bytes('q', 'utf8'))
h.update('ee', bytes('p', 'utf8'))
h.update('he', bytes('visio', 'utf8'))

print(h)
print(memAlloc)
print(h.get('me'))
print(h.get_guts())

try:
    print(h.get('pp'))
except Exception as ex:
    print(ex)
