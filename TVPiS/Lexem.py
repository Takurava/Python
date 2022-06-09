import re
import MemAlloc
import Hash
import Log
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

    def __init__(self, my_type, me, line=-1, num=-1):
        self.type = my_type
        self.me = me
        self.line = line
        self.num = num
        # self.ident_dic = {}

    def __str__(self):
        return f'({self.type} {self.me})'



def create_lexem(memAllock):
    rezerv = {'return': 'return',
              'print': 'print',
              'float': 'float',
              'while': 'while',
              'break': 'break',
              'scan': 'scan',
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
              '/': '/',
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

    it = IterationTokenizer('Code\\1.txt')
    lex = []

    import re
    identifier = r'^[a-zA-Z][\w\d]*$'
    number = r'^[\d]+$|^[\d]+\.[\d]+$'

    for i_line, line in enumerate(it):
        for i_word, word in enumerate(line):
            try:
                lex.append(Lexem(rezerv[word], word, i_line + 1, i_word + 1))
            except KeyError as e:
                if re.match(number, word) is not None:
                    lex.append(Lexem('num', word, i_line + 1, i_word + 1))
                elif re.match(identifier, word) is not None:
                    lex.append(Lexem('var', word, i_line + 1, i_word + 1))
                else:
                    raise NameError(f"Error: unknown token '{word}', line {i_line + 1}, token {i_word + 1} ")
    return lex