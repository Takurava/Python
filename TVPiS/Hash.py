import Log
import MemAlloc
import copy


def fill_mem(mem_alloc, address, bytes_arr):
    segment = mem_alloc.segments[address.segment]
    for i in range(len(bytes_arr)):
        segment[i + address.addr] = bytes_arr[i]


def get_hash(string, size):
    return sum(bytes(string, 'utf8')) % size


class Hash:

    def __init__(self, mem_alloc, max_el_count=4):
        self.mem_alloc = mem_alloc
        self.arr = [[] for i in range(max_el_count)]
        self.max_el_count = max_el_count
        self.el_count = 0

    def update(self, key, value):
        el_address = self.mem_alloc.alloc(len(value))
        fill_mem(self.mem_alloc, el_address, value)
        rewrite_flg = 0
        ind = get_hash(key, self.max_el_count)
        for i in range(len(self.arr[ind])):
            if self.arr[ind][i][0] == key:
                self.mem_alloc.free(self.arr[ind][i][1])
                self.arr[ind].pop(i)
                self.arr[ind].append((key, el_address))
                rewrite_flg = 1
                break

        if rewrite_flg == 0:
            self.arr[ind].append((key, el_address))
            self.el_count = self.el_count + 1

        if self.el_count > 0.75 * self.max_el_count:
            self.new_hash(2 * self.max_el_count)

    def delete(self, key):
        for el in self.arr[get_hash(key, self.max_el_count)]:
            if el[0] == key:
                self.mem_alloc.free(el[1])
                self.arr[get_hash(key, self.max_el_count)].remove(el)
                return

    def new_hash(self, max_el_count):
        arr = copy.deepcopy(self.arr)
        self.arr = [[] for i in range(max_el_count)]
        self.max_el_count = max_el_count
        for mini_arr in arr:
            for key, el_address in mini_arr:
                self.arr[get_hash(key, self.max_el_count)].append((key, el_address))

    def get(self, key):
        ind = get_hash(key, self.max_el_count)
        for k, addr in self.arr[ind]:
            if k == key:
                for mem_block in self.mem_alloc.mem_block_address[addr.segment]:
                    if mem_block.address.segment == addr.segment and mem_block.address.addr == addr.addr:
                        return self.mem_alloc.segments[addr.segment][addr.addr:(addr.addr + mem_block.loc_size)]
        raise NameError(f"KeyError: key '{key}' not found")

    def get_guts(self):
        return str(self.arr)

    def __str__(self):
        result = []
        for mini_arr in self.arr:
            for key, el_address in mini_arr:
                result.append(f'{key}: {str(el_address)}')
        return str(result)

'''
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
'''
