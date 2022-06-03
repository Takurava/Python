import re
import MemAlloc
import Hash
from functools import reduce


def get_all(file_name):
    with open(file_name, 'r') as infile:
        return reduce(lambda a, x: a.extend(x), [inline.split() for inline in infile])


class IterationTokenizer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.infile = open(file_name, 'r')

    def __del__(self):
        self.infile.close()

    def __iter__(self):
        return self

    def __next__(self):
        line = self.infile.readline()
        if not line:
            raise StopIteration
        return line.split()


class Lexem:
    def __init__(self, my_type, me):
        self.type = my_type
        self.me = me

    def __str__(self):
        return f'({self.type} {self.me})'


class Tree:
    def __init__(self, lex, me=None, leafs=None):
        self.lex = lex
        self.me = me
        if leafs is None:
            self.leafs = []
        else:
            self.leafs = leafs

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


rezerv = {'return': 'return',
          'while': 'while',
          'break': 'break',
          'void': 'void',
          'else': 'else',
          'call': 'call',
          'int': 'int',
          'def': 'def',
          'let': 'let',
          'if': 'if',
          '&&': '&&',
          '||': '||',
          '==': '==',
          '!=': '!=',
          '>=': '>=',
          '<=': '<=',
          '\\': '\\',
          '=': '=',
          '<': '>',
          '>': '<',
          '+': '+',
          '-': '-',
          '*': '*',
          '(': '(',
          ')': ')',
          '{': '{',
          '}': '}',
          ';': ';'}


# infile = open('Code\\1.txt', 'r')

memAlloc = MemAlloc.MemAlloc(1024)

h = Hash.Hash(memAlloc)

it = IterationTokenizer('Code\\1.txt')
lex = []

import re
identifier = r'^\w[\w\d]*$'
number = r'^[\d]+$|^[\d]+\.[\d]+$'
identifier_id = 1

for line in it:
    for word in line:
        print(word)
        try:
            lex.append(Lexem(rezerv[word], word))
        except KeyError as e:
            if re.match(number, word) is not None:
                lex.append(Lexem('num', word))
            elif re.match(identifier, word) is not None:
                lex.append(Lexem('var', word))
            else:
                raise NameError(f"Error: unknown lexem '{word}'")


class GramParse:
    def __init__(self, lexems):
        self.lex = lexems
        self.i_lex = 0
        self.tree = None

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
                    if l in ['*', '\\', '-', '+', '==', '!=', '<', '<=', '>', '>=', '&&', '||']:
                        result_lex.append(Tree('<operatoin>', l))
                    elif l not in ['return', 'while', 'break', 'else', 'call', 'def', 'let', 'if']:
                        result_lex.append(l)
                self.i_lex = self.i_lex + 1
            else:
                self.i_lex = remember_i_lex
                return False, None
        return True, result_lex

    def find_gram(self, gram_name):
        if gram_name == '<module>':
            obj = Tree('<module>')
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
                return True, Tree('<function>', leafs=find_obj)
        elif gram_name == '<type>':
            is_find, find_obj = self.try_find(['int'])
            if not is_find:
                is_find, find_obj = self.try_find(['void'])
                if not is_find:
                    return False, None
            return True, Tree('<type>', me=find_obj[0])
        elif gram_name == '<identifier>':
            is_find, find_obj = self.try_find(['var'])
            if not is_find:
                return False, None
            return True, Tree('<identifier>', me=find_obj[0])
        elif gram_name == '<number>':
            is_find, find_obj = self.try_find(['num'])
            if not is_find:
                return False, None
            return True, Tree('<number>', me=find_obj[0])
        elif gram_name == '<arguments>':
            obj = Tree('<arguments>')
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
            return True, Tree('<argument>', leafs=find_obj)
        elif gram_name == '<block>':
            is_find, find_obj = self.try_find(['{'])
            if is_find:
                obj = Tree('<block>')
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
                                    return False, None
            return True, Tree('<statement>', leafs=find_obj)
        elif gram_name == '<declaration>':
            is_find, find_obj = self.try_find(['<type>', '<identifier>', ';'])
            if not is_find:
                return False, None
            return True, Tree('<declaration>', leafs=find_obj)
        elif gram_name == '<assign>':
            is_find, find_obj = self.try_find(['let', '<identifier>', '=', '<expression>', ';'])
            if not is_find:
                return False, None
            return True, Tree('<assign>', leafs=find_obj)
        elif gram_name == '<ifelse>':
            is_find, find_obj = self.try_find(['if', '(', '<condition>', ')', '<block>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<ifelse>', leafs=find_obj)
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
            return True, Tree('<while>', leafs=find_obj)
        elif gram_name == '<jump>':
            is_find, find_obj = self.try_find(['return', '<expression>', ';'])
            if not is_find:
                is_find, find_obj = self.try_find(['break', ';'])
                if not is_find:
                    return False, None
            return True, Tree('<jump>', leafs=find_obj)
        elif gram_name == '<call>':
            is_find, find_obj = self.try_find(['call', '<identifier>', '(', '<expressions>', ')'])
            if not is_find:
                return False, None
            return True, Tree('<call>', leafs=find_obj)
        elif gram_name == '<expressions>':
            obj = Tree('<expressions>')
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
                return True, obj
        elif gram_name == '<comparison>':
            is_find, find_obj = self.try_find(['<expression>'])
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
                return True, obj
        elif gram_name == '<expression>':
            is_find, find_obj = self.try_find(['<term>'])
            if not is_find:
                return False, None
            else:
                obj = Tree('<expression>', leafs=find_obj)
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
                obj = Tree('<term>', leafs=find_obj)
                while True:
                    is_find, find_obj = self.try_find(['*'])
                    if not is_find:
                        is_find, find_obj = self.try_find(['\\'])
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
            obj = Tree('<factor>')
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
                    is_find, find_obj = self.try_find(['(', '<expression>', ')'])
                    if not is_find:
                        return False, None
            obj.add_leafs(find_obj)
            return True, obj
        else:
            raise NameError(f"Error: unknown gram '{gram_name}'")


gp = GramParse(lex)
find, tree = gp.find_gram('<module>')

print(tree)

if gp.i_lex < len(gp.lex):
    raise NameError(f"Error: bad code '{gp.lex[gp.i_lex]}'")
