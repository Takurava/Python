import Log


class Address:
    def __init__(self, segment_id, addr):
        self.segment = segment_id
        self.addr = addr

    def __str__(self):
        return f'Segment - {self.segment}, addr - {self.addr}'


class MemBlock:
    def __init__(self, segment_id, addr, loc_size, is_free=True):
        self.address = Address(segment_id, addr)
        self.loc_size = loc_size
        self.is_free = is_free

    def __str__(self):
        return f'({self.address.segment}, {self.address.addr}, {self.loc_size}, {self.is_free})'  # , {self.prev_addr})'


class MemAlloc:
    def __init__(self, segment_size):
        """Constructor"""
        self.segment_size = segment_size
        self.segments = [[bytes(1) for _i in range(segment_size)]]
        self.mem_block_address = [[MemBlock(0, 0, segment_size, True)]]  # , 0)]

    def __str__(self):
        return f'{self.allocated()}\n' + str([str(block) for segment in self.mem_block_address for block in segment])

    # Find memory place for block of loc_size
    def find_mem(self, loc_size):

        if loc_size > self.segment_size:
            raise NameError(f'Too much! Loc size = {loc_size}')
        else:

            # Try to find memory place in each segments
            for i in range(len(self.segments)):

                prev_addr = MemBlock(i, 0, 0)
                # For each memory block in segment
                for new_mem_block in self.mem_block_address[i]:

                    # If between new block start and previous alloc block end exists loc_size
                    if (new_mem_block.address.addr - (prev_addr.address.addr + prev_addr.loc_size)) >= loc_size:
                        # Return addr for insert block
                        return i, prev_addr.address.addr + prev_addr.loc_size
                    # Else change previous alloc block if new is alloc too
                    elif not new_mem_block.is_free:
                        prev_addr = MemBlock(i, new_mem_block.address.addr, new_mem_block.loc_size)

                # If between last alloc block end end of segment exists loc_size
                if (self.segment_size - (prev_addr.address.addr + prev_addr.loc_size)) >= loc_size:
                    # Return addr for insert block
                    return i, prev_addr.address.addr + prev_addr.loc_size

            # Create new segment if cant find
            segment_id = len(self.segments)
            self.segments.append([bytes(1) for _i in range(self.segment_size)])
            self.mem_block_address.append([MemBlock(segment_id, 0, self.segment_size, True)])
            return segment_id, 0

    # Create lock (and free) block(s) in memory
    def create_segment(self, segment_id, addr, loc_size):

        # For each memory block in segment
        for i in range(len(self.mem_block_address[segment_id])):

            new_mem_block = self.mem_block_address[segment_id][i]
            # If new memory block finished in or after inserted block
            if new_mem_block.address.addr + new_mem_block.loc_size > addr:

                end_of_last_del_mem_block = 0

                # While segment already have other memory block and other block started in inserted block
                while (i < len(self.mem_block_address[segment_id])) \
                        and (self.mem_block_address[segment_id][i].address.addr < addr + loc_size):
                    end_of_last_del_mem_block = self.mem_block_address[segment_id][i].address.addr \
                                                + self.mem_block_address[segment_id][i].loc_size
                    # Delete other memory block
                    del self.mem_block_address[segment_id][i]

                # Create new memory block
                self.mem_block_address[segment_id].append(MemBlock(segment_id, addr, loc_size, False))
                # Create little free memory block
                if addr + loc_size < end_of_last_del_mem_block:
                    free_addr = addr + loc_size
                    free_loc_size = end_of_last_del_mem_block - free_addr
                    self.mem_block_address[segment_id].append(MemBlock(segment_id, free_addr, free_loc_size, True))

    # Try to alloc memory
    def alloc(self, loc_size):
        Log.save(f'Try to alloc memory, Loc size = {loc_size}')

        try:
            # addr, prev_addr = self.find_mem(loc_size)
            segment_id, addr = self.find_mem(loc_size)
            self.create_segment(segment_id, addr, loc_size)  # , prev_addr)

            for segment_address in self.mem_block_address:
                segment_address.sort(key=lambda item: item.address.addr)

            return Address(segment_id, addr)
        except Exception as ex:
            print(ex)

    def free(self, address):
        Log.save(f'Try to free memory, Address = ({address})')

        segment_id = address.segment
        addr = address.addr

        for i in range(len(self.mem_block_address[segment_id])):

            if self.mem_block_address[segment_id][i].address.addr == addr:

                my_i = i
                my_addr = addr
                my_lock_size = self.mem_block_address[segment_id][i].loc_size

                if i < len(self.mem_block_address[segment_id]) - 1 and self.mem_block_address[segment_id][i+1].is_free:
                    my_lock_size = my_lock_size + self.mem_block_address[segment_id][i+1].loc_size
                    del self.mem_block_address[segment_id][i+1]

                if i > 0 and self.mem_block_address[segment_id][i-1].is_free:
                    my_addr = self.mem_block_address[segment_id][i-1].address.addr
                    my_lock_size = my_lock_size + self.mem_block_address[segment_id][i-1].loc_size
                    del self.mem_block_address[segment_id][i-1]
                    my_i = my_i - 1

                self.mem_block_address[segment_id][my_i].address.addr = my_addr
                self.mem_block_address[segment_id][my_i].loc_size = my_lock_size
                self.mem_block_address[segment_id][my_i].is_free = True
                break

    def allocated(self):
        return f'Allocated: {self.segment_size * len(self.segments)} byte(s)'


'''
    def mem_block_info(self):
        return '''


'''
global memAlloc
memAlloc = MemAlloc(1024)
print(memAlloc)

m1 = memAlloc.alloc(4)
m2 = memAlloc.alloc(2)
m3 = memAlloc.alloc(6)
m4 = memAlloc.alloc(1)
m5 = memAlloc.alloc(8)
print(memAlloc)

memAlloc.free(m2[0], m2[1])
memAlloc.free(m4[0], m4[1])
print(memAlloc)

memAlloc.free(m3[0], m3[1])
print(memAlloc)

memAlloc.alloc(1025)
print(memAlloc)

memAlloc.alloc(512)
memAlloc.alloc(512)
memAlloc.alloc(512)
print(memAlloc)
'''
