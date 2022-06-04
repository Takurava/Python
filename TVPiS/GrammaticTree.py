import re
import MemAlloc
import Hash
import Lexem
from functools import reduce


def fill_mem(mem_alloc, address, string):
    bytes_arr = bytes(string, 'utf*')
    segment = mem_alloc.segments[address.segment]
    for i in range(len(bytes_arr)):
        segment[i + address.addr] = bytes_arr[i]


def get_mem(mem_alloc, address):
    for mem_block in mem_alloc.mem_block_address[address.segment]:
        if mem_block.address.segment == address.segment and mem_block.address.addr == address.addr:
            return "".join(map(chr, mem_alloc.segments[address.segment][address.addr:(address.addr + mem_block.loc_size)]))


identifiers_desc = []


class Tree:
    def __init__(self, lex, me=None, leafs=None, memAllock=None):
        self.lex = lex
        self.me = me
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
        gram_name = self.lex
        if gram_name == '<module>':
            result = None
            func = None
            for function in self.leafs:
                if function.leafs[1].me == func_name:
                    func = function
            result = func.run(args=args)
            return result
        elif gram_name == '<function>':
            result = None
            try:
                self.leafs[2].run(args=args)
                self.leafs[3].run()
            except Exception as e:
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
                raise Exception
            num_str = get_mem(self.memAllock, my_str[2])
            if my_str[1].me == 'int':
                return int(num_str)
            elif my_str[1].me == 'float':
                return float(num_str)
        elif gram_name == '<number>':
            rint = r'^[\d]+$'
            rfloat = r'^[\d]+\.[\d]+$'

            if re.match(rint, self.me) is not None:
                return int(self.me)
            elif re.match(rfloat, self.me) is not None:
                return float(self.me)
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
                    raise Exception
                self.memAllock.free(my_str[2])
                identifiers_desc.remove(my_str)
                addr = self.memAllock.alloc(len(bytes(str(arg), 'utf8')))
                identifiers_desc.append((my_str[0], my_str[1], addr))
                fill_mem(self.memAllock, addr, str(arg))
        elif gram_name == '<argument>':
            identifiers_desc.append((self.leafs[1].me, self.leafs[0], self.memAllock.alloc(1)))
        elif gram_name == '<builtin>':
            if self.me == 'scan':
                with open('input.txt', 'r') as read_file:
                    for line in read_file:
                        result = line
                        my_str = None
                        for s in identifiers_desc:
                            if s[0] == self.leafs[0].me:
                                my_str = s
                                break
                        if my_str is None:
                            raise Exception

                        self.memAllock.free(my_str[2])
                        identifiers_desc.remove(my_str)
                        addr = self.memAllock.alloc(len(bytes(str(result), 'utf8')))
                        identifiers_desc.append((my_str[0], my_str[1], addr))
                        fill_mem(self.memAllock, addr, str(result))

            elif self.me == 'print':
                with open('output.txt', 'w') as write_file:
                    write_file.write(str(self.leafs[0].run()))
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
            identifiers_desc.append((self.leafs[1].me, self.leafs[0], self.memAllock.alloc(1)))
        elif gram_name == '<assign>':
            result = self.leafs[1].run()
            my_str = None
            for s in identifiers_desc:
                if s[0] == self.leafs[0].me:
                    my_str = s
                    break
            if my_str is None:
                raise Exception

            self.memAllock.free(my_str[2])
            identifiers_desc.remove(my_str)
            addr = self.memAllock.alloc(len(bytes(str(result), 'utf8')))
            identifiers_desc.append((my_str[0], my_str[1], addr))
            fill_mem(self.memAllock, addr, str(result))
        elif gram_name == '<ifelse>':
            pass
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
            pass
            '''is_find, find_obj = self.try_find(['while', '(', '<condition>', ')', '<block>'])
            if not is_find:
                return False, None
            return True, Tree('<while>', leafs=find_obj)'''
        elif gram_name == '<jump>':
            raise NameError(str(self.leafs[0].run()))
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
            pass
            '''is_find, find_obj = self.try_find(['<comparison>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<condition>', leafs=find_obj)
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
                return True, obj'''
        elif gram_name == '<comparison>':
            pass
            '''is_find, find_obj = self.try_find(['<expression>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<comparison>', leafs=find_obj)
                while True:
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
                                            break
                    obj.add_leafs(find_obj)
                    is_find, find_obj = self.try_find(['<expression>'])
                    if not is_find:
                        return False, None
                    else:
                        obj.add_leafs(find_obj)
                return True, obj'''
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
                    result = result / self.leafs[i*2+2].run()
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
            raise NameError(f"Error: unknown gram '{gram_name}'")
        return True



class GramParse:
    def __init__(self, lexems, memAllock=None):
        self.lex = lexems
        self.i_lex = 0
        self.memAllock = memAllock

    def try_find(self, lexems):
        remember_i_lex = self.i_lex
        result_lex = []
        for l in lexems:
            if re.match(r'^<[\w]*>', l) is not None:
                is_find, find_obj = self.find_gram(l)
                if not is_find:
                    self.i_lex = remember_i_lex
                    return False, None
                else:
                    result_lex.append(find_obj)
            elif self.i_lex >= len(self.lex):
                return False, None
            elif self.lex[self.i_lex].type == l:
                if l not in ['(', ')', '{', '}', ',', ';', '=']:
                    if l in ['*', '/', '-', '+', '==', '!=', '<', '<=', '>', '>=', '&&', '||']:
                        result_lex.append(Tree('<operatoin>', l, memAllock=self.memAllock))
                    elif l not in ['return', 'while', 'break', 'else', 'call', 'def', 'let', 'if']:
                        result_lex.append(self.lex[self.i_lex].type)
                        result_lex.append(self.lex[self.i_lex].me)
                self.i_lex = self.i_lex + 1
            else:
                self.i_lex = remember_i_lex
                return False, None
        return True, result_lex

    def find_gram(self, gram_name, ):
        if gram_name == '<module>':
            obj = Tree('<module>', memAllock=self.memAllock)
            while True:
                is_find, find_obj = self.try_find(['<function>'])
                if not is_find:
                    break
                else:
                    obj.add_leafs(find_obj)
            return True, obj
        elif gram_name == '<function>':
            is_find, find_obj = self.try_find(['def', '<type>', '<identifier>', '(', '<arguments>', ')', '<block>'])
            if not is_find:
                return False, None
            else:
                return True, Tree('<function>', leafs=find_obj, memAllock=self.memAllock)
        elif gram_name == '<type>':
            is_find, find_obj = self.try_find(['int'])
            if not is_find:
                is_find, find_obj = self.try_find(['void'])
                if not is_find:
                    is_find, find_obj = self.try_find(['float'])
                    if not is_find:
                        return False, None
            return True, Tree('<type>', me=find_obj[0], memAllock=self.memAllock)
        elif gram_name == '<identifier>':
            is_find, find_obj = self.try_find(['var'])
            if not is_find:
                return False, None
            return True, Tree('<identifier>', me=find_obj[1], memAllock=self.memAllock)
        elif gram_name == '<number>':
            is_find, find_obj = self.try_find(['num'])
            if not is_find:
                return False, None
            return True, Tree('<number>', me=find_obj[1], memAllock=self.memAllock)
        elif gram_name == '<arguments>':
            obj = Tree('<arguments>', memAllock=self.memAllock)
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
            is_find, find_obj = self.try_find(['<type>', '<identifier>'])
            if not is_find:
                return False, None
            return True, Tree('<argument>', leafs=find_obj, memAllock=self.memAllock)
        elif gram_name == '<builtin>':
            is_find, find_obj = self.try_find(['scan', '(', '<identifier>', ')', ';'])
            if not is_find:
                is_find, find_obj = self.try_find(['print', '(', '<expression>', ')', ';'])
                if not is_find:
                    return False, None
            return True, Tree('<builtin>', me=find_obj[1], leafs=[find_obj[2]], memAllock=self.memAllock)
        elif gram_name == '<block>':
            is_find, find_obj = self.try_find(['{'])
            if is_find:
                obj = Tree('<block>', memAllock=self.memAllock)
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
            return True, Tree('<statement>', leafs=find_obj, memAllock=self.memAllock)
        elif gram_name == '<declaration>':
            is_find, find_obj = self.try_find(['<type>', '<identifier>', ';'])
            if not is_find:
                return False, None
            return True, Tree('<declaration>', leafs=find_obj, memAllock=self.memAllock)
        elif gram_name == '<assign>':
            is_find, find_obj = self.try_find(['let', '<identifier>', '=', '<expression>', ';'])
            if not is_find:
                return False, None
            return True, Tree('<assign>', leafs=find_obj, memAllock=self.memAllock)
        elif gram_name == '<ifelse>':
            is_find, find_obj = self.try_find(['if', '(', '<condition>', ')', '<block>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<ifelse>', leafs=find_obj, memAllock=self.memAllock)
                is_find, find_obj = self.try_find(['else', '<block>'])
                if not is_find:
                    return True, obj
                else:
                    obj.add_leafs(find_obj)
                    return True, obj
        elif gram_name == '<while>':
            is_find, find_obj = self.try_find(['while', '(', '<condition>', ')', '<block>'])
            if not is_find:
                return False, None
            return True, Tree('<while>', leafs=find_obj, memAllock=self.memAllock)
        elif gram_name == '<jump>':
            is_find, find_obj = self.try_find(['return', '<expression>', ';'])
            if not is_find:
                is_find, find_obj = self.try_find(['break', ';'])
                if not is_find:
                    return False, None
            return True, Tree('<jump>', leafs=find_obj, memAllock=self.memAllock)
        elif gram_name == '<call>':
            is_find, find_obj = self.try_find(['call', '<identifier>', '(', '<expressions>', ')'])
            if not is_find:
                return False, None
            return True, Tree('<call>', leafs=find_obj, memAllock=self.memAllock)
        elif gram_name == '<expressions>':
            obj = Tree('<expressions>', memAllock=self.memAllock)
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
            is_find, find_obj = self.try_find(['<comparison>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<condition>', leafs=find_obj, memAllock=self.memAllock)
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
            is_find, find_obj = self.try_find(['<expression>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<comparison>', leafs=find_obj, memAllock=self.memAllock)
                while True:
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
                                            break
                    obj.add_leafs(find_obj)
                    is_find, find_obj = self.try_find(['<expression>'])
                    if not is_find:
                        return False, None
                    else:
                        obj.add_leafs(find_obj)
                return True, obj
        elif gram_name == '<expression>':
            is_find, find_obj = self.try_find(['<term>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<expression>', leafs=find_obj, memAllock=self.memAllock)
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
            is_find, find_obj = self.try_find(['<factor>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<term>', leafs=find_obj, memAllock=self.memAllock)
                while True:
                    is_find, find_obj = self.try_find(['*'])
                    if not is_find:
                        is_find, find_obj = self.try_find(['//'])
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
            obj = Tree('<factor>', memAllock=self.memAllock)
            is_find, find_obj = self.try_find(['+'])
            if not is_find:
                is_find, find_obj = self.try_find(['-'])
                if not is_find:
                    pass
            if is_find:
                obj.add_leafs(find_obj)

            is_find, find_obj = self.try_find(['<number>'])
            if not is_find:
                is_find, find_obj = self.try_find(['<identifier>'])
                if not is_find:
                    is_find, find_obj = self.try_find(['<call>'])
                    if not is_find:
                        is_find, find_obj = self.try_find(['(', '<expression>', ')'])
                        if not is_find:
                            return False, None
            obj.add_leafs(find_obj)
            return True, obj
        else:
            raise NameError(f"Error: unknown gram '{gram_name}'")
