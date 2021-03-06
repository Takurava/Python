import re
import MemAlloc
import Hash
import Stack
import Log
from functools import reduce
import codecs


def fill_mem(mem_alloc, address, string):
    bytes_arr = bytes(string, 'utf*')
    segment = mem_alloc.segments[address.segment]
    for i in range(len(bytes_arr)):
        segment[i + address.addr] = bytes_arr[i]


def get_mem(mem_alloc, address):
    for mem_block in mem_alloc.mem_block_address[address.segment]:
        if mem_block.address.segment == address.segment and mem_block.address.addr == address.addr:
            try:
                return "".join(map(chr, mem_alloc.segments[address.segment][address.addr:(address.addr + mem_block.loc_size)]))
            except Exception as e:
                return '-1'


scan_queue = Stack.Deque(mem_alloc=MemAlloc.MemAlloc(1024))
with open('input.txt', 'r') as read_file:
    for line in read_file:
        for word in line.split():
            scan_queue.push_back(bytes(str(word), 'utf8'))
with open('output.txt', 'w') as write_file:
    pass

identifiers_desc = []
h = [(0, Hash.Hash(mem_alloc=MemAlloc.MemAlloc(1024)))]
identifier_id = 0
deep = 0
local_deep = 0


class Tree:
    def __init__(self, lex, me=None, leafs=None, memAllock=None, i_lex=-1, lesems=[]):
        self.lex = lex
        self.lexems = lesems
        self.me = me
        self.i_lex = i_lex
        if leafs is None:
            self.leafs = []
        else:
            self.leafs = leafs
        self.memAllock = memAllock

    def get_str(self, deep=0):
        result = ""
        if self.me is not None:
            result = '    '*deep + f'({self.lex} {self.me})' + '\n'
        else:
            result = '    ' * deep + f'({self.lex})' + '\n'
        for leaf in self.leafs:
            result = result + leaf.get_str(deep+1)
        return result

    def __str__(self):
        return self.get_str()

    def add_leafs(self, leafs):
        self.leafs.extend(leafs)

    def run(self, func_name=None, args=None):
        global deep
        gram_name = self.lex
        if gram_name == '<module>':
            result = None
            func = None
            for function in self.leafs:
                if function.leafs[1].me == func_name:
                    func = function
            result = func.run(args=args)
            for desc in identifiers_desc:
                Log.save(f'{desc[0]} {desc[1].me} {get_mem(self.memAllock, desc[2])}')
            return
        elif gram_name == '<function>':
            result = None
            try:
                self.leafs[2].run(args=args)
                self.leafs[3].run()
            except NameError as e:
                result = str(e)
            return result
            '''self.leafs[2].run(args=args)
            self.leafs[3].run()'''
        elif gram_name == '<type>':
            pass
            '''is_find, find_obj = self.try_find(['int'])
            if not is_find:
                is_find, find_obj = self.try_find(['void'])
                if not is_find:
                    return False, None
            return True, Tree('<type>', me=find_obj[0])'''
        elif gram_name == '<identifier>':
            my_str = None
            for s in identifiers_desc:
                if s[0] == self.me:
                    my_str = s
                    break
            if my_str is None:
                raise Exception(f"unknown identifier {self.lexems[self.i_lex].me}, line {self.lexems[self.i_lex].line}, token {self.lexems[self.i_lex].num}")
            num_str = get_mem(self.memAllock, my_str[2])
            if my_str[1].me == 'num':
                return float(num_str)
            elif my_str[1].me == 'str':
                return num_str
        elif gram_name == '<number>':
            return float(self.me)
        elif gram_name == '<string>':
            return self.me
        elif gram_name == '<arguments>':
            for i in range(len(self.leafs)):
                argument = self.leafs[i]
                argument.run()
                arg = args[i]
                my_str = None
                for s in identifiers_desc:
                    if s[0] == self.leafs[i].leafs[1].me:
                        my_str = s
                        break
                if my_str is None:
                    raise Exception(f"unknown argument {self.lexems[self.i_lex+1].me}, line {self.lexems[self.i_lex+1].line}, token {self.lexems[self.i_lex+1].num}")
                self.memAllock.free(my_str[2])
                identifiers_desc.remove(my_str)
                addr = self.memAllock.alloc(len(bytes(str(arg), 'utf8')))
                identifiers_desc.append((my_str[0], my_str[1], addr, my_str[3]))
                fill_mem(self.memAllock, addr, str(arg))
        elif gram_name == '<argument>':
            identifiers_desc.append((self.leafs[1].me, self.leafs[0], self.memAllock.alloc(1)))
        elif gram_name == '<builtin>':
            if self.me == 'scan':
                result = "".join(map(chr, scan_queue.pop_front()))
                my_str = None
                for s in identifiers_desc:
                    if s[0] == self.leafs[0].me:
                        my_str = s
                        break
                if my_str is None:
                    raise Exception(f"unknown identifier {self.lexems[self.i_lex+2].me}, line {self.lexems[self.i_lex+2].line}, token {self.lexems[self.i_lex+2].num}")

                self.memAllock.free(my_str[2])
                identifiers_desc.remove(my_str)
                addr = self.memAllock.alloc(len(bytes(str(result), 'utf8')))
                identifiers_desc.append((my_str[0], my_str[1], addr, my_str[3]))
                fill_mem(self.memAllock, addr, str(result))

            elif self.me == 'print':
                with open('output.txt', 'a') as write_file:
                    write_file.write(str(self.leafs[0].run())+'\n')
            elif self.me == 'exit':
                exit(str(self.leafs[0].run()))
            '''if 
            with open(f'input.txt', 'r') as read_file:
                for line in  read_file:
                    
            is_find, find_obj = self.try_find(['scan', '(', '<identifier>', ')', ';'])
            if not is_find:
                is_find, find_obj = self.try_find(['print', '(', '<identifier>', ')', ';'])
                if not is_find:
                    return False, None
            return True, Tree('<builtin>', leafs=find_obj, memAllock=self.memAllock)'''
        elif gram_name == '<block>':
            for statement in self.leafs:
                statement.run('<statement>')
        elif gram_name == '<statement>':
            for leaf in self.leafs:
                leaf.run()
        elif gram_name == '<declaration>':
            identifiers_desc.append((self.leafs[1].me, self.leafs[0], self.memAllock.alloc(1), deep))
        elif gram_name == '<assign>':
            result = self.leafs[1].run()
            my_str = None
            for s in identifiers_desc:
                if s[0] == self.leafs[0].me:
                    my_str = s
                    break
            if my_str is None:
                raise Exception(
                    f"unknown identifier {self.lexems[self.i_lex+1].me}, line {self.lexems[self.i_lex+1].line}, token {self.lexems[self.i_lex+1].num}")

            self.memAllock.free(my_str[2])
            identifiers_desc.remove(my_str)
            addr = self.memAllock.alloc(len(bytes(str(result), 'utf8')))
            identifiers_desc.append((my_str[0], my_str[1], addr, my_str[3]))
            fill_mem(self.memAllock, addr, str(result))
        elif gram_name == '<ifelse>':
            if self.leafs[0].run() > 0:
                last_deep = deep
                deep = self.me
                self.leafs[1].run()
                while True:
                    el = None
                    for e in identifiers_desc:
                        if e[3] == deep:
                            el = e
                            break
                    if el is None:
                        break
                    identifiers_desc.remove(el)
                deep = last_deep
            else:
                last_deep = deep
                deep = self.leafs[2].me
                self.leafs[2].run()
                while True:
                    el = None
                    for e in identifiers_desc:
                        if e[3] == deep:
                            el = e
                            break
                    if el is None:
                        break
                    identifiers_desc.remove(el)
                deep = last_deep
            '''is_find, find_obj = self.try_find(['if', '(', '<condition>', ')', '<block>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<ifelse>', leafs=find_obj)
                is_find, find_obj = self.try_find(['else', '<block>'])
                if not is_find:
                    return True, obj
                else:
                    obj.add_leafs(find_obj)
                    return True, obj'''
        elif gram_name == '<while>':
            while True:
                try:
                    last_deep = deep
                    deep = self.me
                    self.leafs[0].run()
                    while True:
                        el = None
                        for e in identifiers_desc:
                            if e[3] == self.me:
                                el = e
                                break
                        if el is None:
                            break
                        identifiers_desc.remove(el)
                    deep = last_deep
                except NameError as e:
                    break
            '''is_find, find_obj = self.try_find(['while', '<block>'])
            if not is_find:
                return False, None
            return True, Tree('<while>', leafs=find_obj)'''
        elif gram_name == '<jump>':
            if len(self.leafs) > 0:
                raise NameError(str(self.leafs[0].run()))
            else:
                raise NameError(None)
        elif gram_name == '<call>':
            pass
            '''is_find, find_obj = self.try_find(['call', '<identifier>', '(', '<expressions>', ')'])
            if not is_find:
                return False, None
            return True, Tree('<call>', leafs=find_obj)'''
        elif gram_name == '<expressions>':
            pass
            '''obj = Tree('<expressions>')
            is_find, find_obj = self.try_find(['<expression>'])
            if not is_find:
                return True, obj
            else:
                obj.add_leafs(find_obj)
                while True:
                    is_find, find_obj = self.try_find([',', '<expression>'])
                    if not is_find:
                        break
                    else:
                        obj.add_leafs(find_obj)
                return True, obj'''
        elif gram_name == '<condition>':
            result = self.leafs[0].run()
            for i in range(int(len(self.leafs) / 2)):
                if self.leafs[i * 2 + 1].me == '&&':
                    result = result * self.leafs[i * 2 + 2].run()
                elif self.leafs[i * 2 + 1].me == '||':
                    result = result + self.leafs[i * 2 + 2].run()
            if result >= 1:
                return 1
            else:
                return 0
        elif gram_name == '<comparison>':
            result = self.leafs[0].run()

            if len(self.leafs) > 1:
                result2 = self.leafs[2].run()
                operation = self.leafs[1].me
                if operation == '==':
                    return result == result2
                elif operation == '!=':
                    return result != result2
                elif operation == '>':
                    return result > result2
                elif operation == '>=':
                    return result >= result2
                elif operation == '<':
                    return result < result2
                elif operation == '<=':
                    return result <= result2

            if result >= 1:
                return 1
            else:
                return 0
        elif gram_name == '<expression>':
            result = self.leafs[0].run()
            for i in range(int(len(self.leafs)/2)):
                if self.leafs[i*2+1].me == '+':
                    result = result + self.leafs[i*2+2].run()
                elif self.leafs[i*2+1].me == '-':
                    result = result - self.leafs[i*2+2].run()
            return result
        elif gram_name == '<term>':
            result = self.leafs[0].run()
            for i in range(int(len(self.leafs)/2)):
                if self.leafs[i*2+1].me == '*':
                    result = result * self.leafs[i*2+2].run()
                elif self.leafs[i*2+1].me == '/':
                    denominator = self.leafs[i*2+2].run()
                    if denominator == 0:
                        raise ZeroDivisionError(f"line {self.me}")
                    else:
                        result = result / denominator
            return result
        elif gram_name == '<factor>':
            result = None
            if self.leafs[0].me == '-':
                result = - self.leafs[1].run()
            elif self.leafs[0].me == '+':
                result = self.leafs[1].run()
            else:
                result = self.leafs[0].run()
            return result
        else:
            raise Exception(f"Error: unknown gram '{gram_name}'")
        return True



class GramParse:
    def __init__(self, lexems, memAllock=None):
        self.lex = lexems
        self.i_lex = 0
        self.max_i_lex = 0
        self.memAllock = memAllock

    def try_find(self, lexems):
        remember_i_lex = self.i_lex
        result_lex = []
        for l in lexems:
            if re.match(r'^<[\w]*>', l) is not None:
                is_find, find_obj = self.find_gram(l)
                if not is_find:
                    if self.max_i_lex < self.i_lex:
                        self.max_i_lex = self.i_lex
                    self.i_lex = remember_i_lex
                    return False, None
                else:
                    result_lex.append(find_obj)
            elif self.i_lex >= len(self.lex):
                self.max_i_lex = len(self.lex) - 1
                return False, None
            elif self.lex[self.i_lex].type == l:
                if l not in ['(', ')', '{', '}', ',', ';', '=']:
                    if l in ['*', '/', '-', '+', '==', '!=', '<', '<=', '>', '>=', '&&', '||']:
                        result_lex.append(Tree('<operatoin>', l, memAllock=self.memAllock, i_lex=self.i_lex, lesems=self.lex))
                    elif l not in ['return', 'while', 'break', 'else', 'call', 'def', 'let', 'if']:
                        result_lex.append(self.lex[self.i_lex].type)
                        result_lex.append(self.lex[self.i_lex].me)
                self.i_lex = self.i_lex + 1
            else:
                if self.max_i_lex < self.i_lex:
                    self.max_i_lex = self.i_lex
                self.i_lex = remember_i_lex
                return False, None
        return True, result_lex

    def find_gram(self, gram_name, ):
        global deep
        global local_deep
        if gram_name == '<module>':
            obj = Tree('<module>', memAllock=self.memAllock, i_lex=self.i_lex, lesems=self.lex)
            while True:
                is_find, find_obj = self.try_find(['<function>'])
                if not is_find:
                    break
                else:
                    obj.add_leafs(find_obj)
            deep = 0
            return True, obj
        elif gram_name == '<function>':
            i_lex = self.i_lex
            is_find, find_obj = self.try_find(['def', '<type>', '<identifier>', '(', '<arguments>', ')', '<block>'])
            if not is_find:
                return False, None
            else:
                return True, Tree('<function>', memAllock=self.memAllock, leafs=find_obj, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<type>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['num'])
            if not is_find:
                is_find, find_obj = self.try_find(['void'])
                if not is_find:
                    is_find, find_obj = self.try_find(['str'])
                    if not is_find:
                        return False, None
            return True, Tree('<type>', me=find_obj[0], memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<identifier>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['var'])
            if not is_find:
                return False, None
            return True, Tree('<identifier>', me=find_obj[1], memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<number>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['num'])
            if not is_find:
                return False, None
            return True, Tree('<number>', me=find_obj[1], memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<string>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['str'])
            if not is_find:
                return False, None
            return True, Tree('<string>', me=find_obj[1], memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<arguments>':
            obj = Tree('<arguments>', memAllock=self.memAllock, i_lex=self.i_lex, lesems=self.lex)
            is_find, find_obj = self.try_find(['<argument>'])
            if not is_find:
                return True, obj
            else:
                obj.add_leafs(find_obj)
                while True:
                    is_find, find_obj = self.try_find([',', '<argument>'])
                    if not is_find:
                        break
                    else:
                        obj.add_leafs(find_obj)
                return True, obj
        elif gram_name == '<argument>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['<type>', '<identifier>'])
            if not is_find:
                return False, None
            word = find_obj[1].me
            try:
                word_id = "".join(map(chr, h[deep].get(word)))
                find_obj[1].me = word_id
            except KeyError as e:
                raise Exception(
                    f"unknown identifier {word}, line {self.lex[i_lex + 1].line}, token {self.lex[i_lex + 1].num}")
            return True, Tree('<argument>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<builtin>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['scan', '(', '<identifier>', ')', ';'])
            if not is_find:
                is_find, find_obj = self.try_find(['print', '(', '<expression>', ')', ';'])
                if not is_find:
                    is_find, find_obj = self.try_find(['exit', '(', '<number>', ')', ';'])
                    if not is_find:
                        return False, None
            else:
                word = find_obj[2].me
                word_id = None
                lc_deep = local_deep
                for i_h in range(deep, -1, -1):
                    hash = h[i_h]
                    if hash[0] <= lc_deep:
                        try:
                            word_id = "".join(map(chr, hash[1].get(word)))
                            find_obj[2].me = word_id
                            break
                        except KeyError as e:
                            lc_deep = lc_deep - 1
                if word_id is None:
                    raise Exception(
                        f"unknown identifier {word}, line {self.lex[i_lex + 2].line}, token {self.lex[i_lex + 2].num}")
            return True, Tree('<builtin>', me=find_obj[1], leafs=[find_obj[2]], memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<block>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['{'])
            if is_find:
                obj = Tree('<block>', memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
                while True:
                    is_find, find_obj = self.try_find(['<statement>'])
                    if not is_find:
                        break
                    else:
                        obj.add_leafs(find_obj)
                is_find, find_obj = self.try_find(['}'])
                if is_find:
                    return True, obj
                return False, None
            return False, None
        elif gram_name == '<statement>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['<declaration>'])
            if not is_find:
                is_find, find_obj = self.try_find(['<assign>'])
                if not is_find:
                    is_find, find_obj = self.try_find(['<ifelse>'])
                    if not is_find:
                        is_find, find_obj = self.try_find(['<while>'])
                        if not is_find:
                            is_find, find_obj = self.try_find(['<jump>'])
                            if not is_find:
                                is_find, find_obj = self.try_find(['<call>'])
                                if not is_find:
                                    is_find, find_obj = self.try_find(['<builtin>'])
                                    if not is_find:
                                        return False, None
            return True, Tree('<statement>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<declaration>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['<type>', '<identifier>', ';'])
            if not is_find:
                return False, None
            word = find_obj[1].me
            global identifier_id
            try:
                h[deep][1].get(word)
                raise Exception(f"repeated declaration of identifier {find_obj[1].me}, line {self.lex[i_lex + 1].line}, token {self.lex[i_lex + 1].num}")
            except KeyError as e:
                h[deep][1].update(word, bytes(str(identifier_id), 'utf8'))
                word_id = str(identifier_id)
                Log.save(f'{word} is {identifier_id}')
                identifier_id = identifier_id + 1
            find_obj[1].me = word_id
            return True, Tree('<declaration>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<assign>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['let', '<identifier>', '=', '<expression>', ';'])
            if not is_find:
                return False, None
            word = find_obj[0].me
            word_id = None
            lc_deep = local_deep
            for i_h in range(deep, -1, -1):
                hash = h[i_h]
                if hash[0] <= lc_deep:
                    try:
                        word_id = "".join(map(chr, hash[1].get(word)))
                        find_obj[0].me = word_id
                        break
                    except KeyError as e:
                        lc_deep = lc_deep - 1
            if word_id is None:
                raise Exception(
                        f"unknown identifier {word}, line {self.lex[i_lex + 1].line}, token {self.lex[i_lex + 1].num}")
            return True, Tree('<assign>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<ifelse>':
            i_lex=self.i_lex
            local_deep = local_deep + 1
            deep = deep + 1
            ll_deep = deep
            h.append((local_deep, Hash.Hash(mem_alloc=MemAlloc.MemAlloc(1024))))
            is_find, find_obj = self.try_find(['if', '(', '<condition>', ')', '<block>'])
            if not is_find:
                h.pop(len(h)-1)
                deep = deep - 1
                local_deep = local_deep - 1
                return False, None
            else:
                local_deep = local_deep - 1

                local_deep = local_deep + 1
                deep = deep + 1
                ll_deep = deep
                h.append((local_deep, Hash.Hash(mem_alloc=MemAlloc.MemAlloc(1024))))
                obj = Tree('<ifelse>', leafs=find_obj, me=ll_deep, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
                is_find, find_obj = self.try_find(['else', '<block>'])
                if not is_find:
                    h.pop(len(h) - 1)
                    deep = deep - 1
                    local_deep = local_deep - 1
                    return True, obj
                else:
                    find_obj[0].me = deep
                    local_deep = local_deep - 1
                    obj.add_leafs(find_obj)
                    return True, obj
        elif gram_name == '<while>':
            i_lex=self.i_lex
            local_deep = local_deep + 1
            deep = deep + 1
            ll_deep = deep
            h.append((local_deep, Hash.Hash(mem_alloc=MemAlloc.MemAlloc(1024))))
            is_find, find_obj = self.try_find(['while', '<block>'])
            if not is_find:
                deep = deep - 1
                local_deep = local_deep - 1
                h.pop(len(h)-1)
                return False, None
            local_deep = local_deep - 1
            return True, Tree('<while>', me=ll_deep, leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<jump>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['return', '<expression>', ';'])
            if not is_find:
                is_find, find_obj = self.try_find(['break', ';'])
                if not is_find:
                    return False, None
            return True, Tree('<jump>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<call>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['call', '<identifier>', '(', '<expressions>', ')'])
            if not is_find:
                return False, None
            word = find_obj[0].me
            try:
                word_id = "".join(map(chr, h[deep].get(word)))
                find_obj[0].me = word_id
            except KeyError as e:
                raise Exception(
                    f"unknown identifier {word}, line {self.lex[i_lex + 1].line}, token {self.lex[i_lex + 1].num}")
            return True, Tree('<call>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
        elif gram_name == '<expressions>':
            obj = Tree('<expressions>', memAllock=self.memAllock, i_lex=self.i_lex, lesems=self.lex)
            is_find, find_obj = self.try_find(['<expression>'])
            if not is_find:
                return True, obj
            else:
                obj.add_leafs(find_obj)
                while True:
                    is_find, find_obj = self.try_find([',', '<expression>'])
                    if not is_find:
                        break
                    else:
                        obj.add_leafs(find_obj)
                return True, obj
        elif gram_name == '<condition>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['<comparison>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<condition>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
                while True:
                    is_find, find_obj = self.try_find(['&&'])
                    if not is_find:
                        is_find, find_obj = self.try_find(['||'])
                        if not is_find:
                            break
                    obj.add_leafs(find_obj)
                    is_find, find_obj = self.try_find(['<comparison>'])
                    if not is_find:
                        return False, None
                    else:
                        obj.add_leafs(find_obj)
                return True, obj
        elif gram_name == '<comparison>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['<expression>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<comparison>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
                is_find, find_obj = self.try_find(['=='])
                if not is_find:
                    is_find, find_obj = self.try_find(['!='])
                    if not is_find:
                        is_find, find_obj = self.try_find(['>'])
                        if not is_find:
                            is_find, find_obj = self.try_find(['>='])
                            if not is_find:
                                is_find, find_obj = self.try_find(['<'])
                                if not is_find:
                                    is_find, find_obj = self.try_find(['<='])
                                    if not is_find:
                                        return True, obj
                obj.add_leafs(find_obj)
                is_find, find_obj = self.try_find(['<expression>'])
                if not is_find:
                    return False, None
                else:
                    obj.add_leafs(find_obj)
                return True, obj
        elif gram_name == '<expression>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['<term>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<expression>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
                while True:
                    is_find, find_obj = self.try_find(['+'])
                    if not is_find:
                        is_find, find_obj = self.try_find(['-'])
                        if not is_find:
                            break
                    obj.add_leafs(find_obj)
                    is_find, find_obj = self.try_find(['<term>'])
                    if not is_find:
                        return False, None
                    else:
                        obj.add_leafs(find_obj)
                return True, obj
        elif gram_name == '<term>':
            i_lex=self.i_lex
            is_find, find_obj = self.try_find(['<factor>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<term>', leafs=find_obj, memAllock=self.memAllock, i_lex=i_lex, lesems=self.lex)
                while True:
                    is_find, find_obj = self.try_find(['*'])
                    if not is_find:
                        is_find, find_obj = self.try_find(['/'])
                        if not is_find:
                            break
                    obj.add_leafs(find_obj)
                    is_find, find_obj = self.try_find(['<factor>'])
                    if not is_find:
                        return False, None
                    else:
                        obj.add_leafs(find_obj)
                return True, obj
        elif gram_name == '<factor>':
            obj = Tree('<factor>', memAllock=self.memAllock, i_lex=self.i_lex, lesems=self.lex)
            is_find, find_obj = self.try_find(['+'])
            if not is_find:
                is_find, find_obj = self.try_find(['-'])
                if not is_find:
                    pass
            if is_find:
                obj.add_leafs(find_obj)

            is_find, find_obj = self.try_find(['<number>'])
            if not is_find:
                is_find, find_obj = self.try_find(['<string>'])
                if not is_find:
                    is_find, find_obj = self.try_find(['<identifier>'])
                    if not is_find:
                        is_find, find_obj = self.try_find(['<call>'])
                        if not is_find:
                            is_find, find_obj = self.try_find(['(', '<expression>', ')'])
                            if not is_find:
                                return False, None
                    else:
                        word = find_obj[0].me
                        word_id = None
                        lc_deep = local_deep
                        for i_h in range(deep, -1, -1):
                            hash = h[i_h]
                            if hash[0] <= lc_deep:
                                try:
                                    word_id = "".join(map(chr, hash[1].get(word)))
                                    find_obj[0].me = word_id
                                    break
                                except KeyError as e:
                                    lc_deep = lc_deep - 1
                        if word_id is None:
                            raise Exception(
                                f"unknown identifier {word}, line {self.lex[find_obj[0].i_lex].line}, token {self.lex[find_obj[0].i_lex].num}")
            obj.add_leafs(find_obj)
            return True, obj
        else:
            raise Exception(f"Error: unknown gram '{gram_name}'")
