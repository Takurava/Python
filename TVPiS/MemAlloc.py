class MemBlock:
    def __init__(self, addr, loc_size, is_free, prev_addr):
        self.addr = addr
        self.loc_size = loc_size
        self.is_free = is_free
        self.prev_addr = prev_addr

    def __str__(self):
        return f'({self.addr}, {self.loc_size}, {self.is_free}, {self.prev_addr})'


class MemAlloc:
    def __init__(self, arr_size):
        """Constructor"""
        self.arr = [bytes(1) for _i in range(arr_size)]
        self.address = [MemBlock(0, arr_size, True, 0)]

    def __str__(self):
        return f'Lock: {str(self.allocated())}\n'+ str([str(item) for item in self.address])

    def find_mem(self, loc_size):

        prev_addr = (0, 0)
        for new_mem_block in self.address:
            if (new_mem_block.addr - (prev_addr[0] + prev_addr[1])) >= loc_size:
                prev_addr = (new_mem_block.addr, new_mem_block.loc_size)
                break
            elif not new_mem_block.is_free:
                prev_addr = (new_mem_block.addr, new_mem_block.loc_size)

        if (prev_addr[0] + prev_addr[1] + loc_size - 1) >= len(self.arr):
            raise NameError(f'Too much! Loc size = {loc_size}')
        else:
            return prev_addr[0] + prev_addr[1], prev_addr[0]

    def create_segment(self, addr, loc_size, prev_addr):
        for i in range(len(self.address)):
            if self.address[i].addr + self.address[i].loc_size > addr:

                end_of_last_del_mem_block = 0
                while (i < len(self.address)) and (self.address[i].addr < addr + loc_size):
                    end_of_last_del_mem_block = self.address[i].addr + self.address[i].loc_size
                    del self.address[i]

                self.address.append(MemBlock(addr, loc_size, False, prev_addr))
                if addr + loc_size - 1 < end_of_last_del_mem_block:
                    free_addr = addr + loc_size
                    free_loc_size = end_of_last_del_mem_block - free_addr + 1
                    self.address.append(MemBlock(free_addr, free_loc_size, True, addr))

    def alloc(self, loc_size):

        try:
            addr, prev_addr = self.find_mem(loc_size)
            self.create_segment(addr, loc_size, prev_addr)

            self.address.sort(key=lambda item: item.addr)

            return addr
        except Exception as ex:
            print(ex)

    def free(self, addr):
        for i in range(len(self.address)):
            if self.address[i].addr == addr:
                self.address[i].is_free = True
                break

    def allocated(self):
        return sum([block.loc_size if not block.is_free else 0 for block in self.address])


memAlloc = MemAlloc(1024)
print(memAlloc)

memAlloc.alloc(4)
memAlloc.alloc(2)
memAlloc.alloc(6)
memAlloc.alloc(1)
memAlloc.alloc(8)
print(memAlloc)

memAlloc.free(4)
memAlloc.free(12)
print(memAlloc)

memAlloc.free(6)
print(memAlloc)

memAlloc.alloc(1000)
print(memAlloc)

memAlloc.alloc(14)
print(memAlloc)

memAlloc.alloc(7)
memAlloc.alloc(7)
print(memAlloc)
